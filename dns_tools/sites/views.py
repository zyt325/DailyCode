from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from dns.LdapBackend import LDAPBackend
from dwebsocket.decorators import accept_websocket, require_websocket


def check_login(fn):
    def wrapper(request, *args, **kwargs):
        # request.session.clear()
        request.session.clear_expired()
        print(request.session.get_expiry_date())
        if request.session.get('is_login_dns_username', False):
            return fn(request, *args, *kwargs)
        else:
            return redirect('sites:login')

    return wrapper


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = LDAPBackend().authenticate(username, password)
        print(username, password, user)
        if user:
            request.session['is_login_dns_username'] = True
            request.session.set_expiry(86400)
            request.session['username'] = username
            return redirect('sites:index')
        else:
            return render(request, 'login.html', {'notify': 'authentication failed'})
    else:
        request.session.clear_expired()
        if request.session.get('is_login_dns_username', False):
            return redirect('sites:index')
        return render(request, 'login.html')

def logout(request):
    request.session.clear_expired()
    request.session.flush()
    return redirect('sites:login')

# Create your views here.
@check_login
def index(request):
    username=request.session.get('username',False)
    return render(request, 'index.html', context=locals())


# init
def zones_menu(request):
    from .models import DnsToolBindzones
    zones = DnsToolBindzones.objects.using("dns").filter(type='Forward').order_by('parent_to_id', 'city').values('id',
                                                                                                                 'zone_name',
                                                                                                                 'city',
                                                                                                                 'parent_to')
    # print(zones.query)
    result = []
    result_name = []
    for item in list(zones):
        # print(item)
        if item['parent_to'] == None and item['zone_name'] not in result_name:
            result_name.append(item['zone_name'])
            result.append(
                {'id': item['zone_name'], 'parent': '#', 'text': item['zone_name'], 'state': {'opened': True}})
            result.append({'id': item['id'], 'parent': item['zone_name'], 'text': item['city']})
        elif item['zone_name'] in result_name:
            result.append({'id': item['id'], 'parent': item['zone_name'], 'text': item['city']})
        else:
            result.append({'id': item['id'], 'parent': item['parent_to'], 'text': item['zone_name']})
    return JsonResponse(result, safe=False)


def str_to_bool(str):
    return True if str.lower() == 'true' else False


def rr_search(request):
    import json
    from .models import DnsRrs, DnsToolBindzones
    from django.db.models import Q
    from django.core.paginator import Paginator
    from django.core import serializers
    direction = request.GET.get('direction', 'Forward')
    zone_name = request.GET.get('zone_name', 'com')
    zone_id = request.GET.get('zone_id', 0)
    search_text = request.GET.get('search', 0)
    filter = request.GET.get('filter', {})
    fuzzy = str_to_bool(request.GET.get('fuzzy', 'True'))
    sort = request.GET.get('sort', 'name')
    sort_order = request.GET.get('order', 'asc')
    if sort_order == 'asc':
        rrs = DnsRrs.objects.using("dns").filter(Q(direction=direction)).order_by('%s' % sort)
    else:
        rrs = DnsRrs.objects.using("dns").filter(Q(direction=direction)).order_by('-%s' % sort)
    # print(fuzzy,type(fuzzy))
    if not zone_id:
        rrs = rrs.filter(Q(zone_name__icontains=zone_name))
    else:
        child_zone_names = DnsToolBindzones.objects.using("dns").filter(parent_to=zone_id).values('zone_name')
        rrs = rrs.filter((Q(zone_name__in=child_zone_names) | Q(zone_id=zone_id)))
    if search_text and fuzzy:
        rrs = rrs.filter((Q(name__icontains=search_text) | Q(value__icontains=search_text)))
    elif search_text and not fuzzy:
        rrs = rrs.filter((Q(name=search_text) | Q(value=search_text)))
    if filter: filter = json.loads(filter)
    for k, v in filter.items():
        if k == 'type':
            rrs = rrs.filter(type=v)
        elif k == 'zone':
            rrs = rrs.filter(zone_name__icontains='.'.join(v.split('.')[:-1]))
            rrs = rrs.filter(city=v.split('.')[-1])
        elif k == 'name' and fuzzy:
            rrs = rrs.filter(name__icontains=v)
        elif k == 'name' and not fuzzy:
            print(1)
            rrs = rrs.filter(name=v)
        elif k == 'value' and fuzzy:
            rrs = rrs.filter(value__icontains=v)
        else:
            rrs = rrs.filter(value=v)
    page_limit = request.GET.get('limit', 15)
    page_offset = request.GET.get('offset', 0)
    if not page_offset:
        page = 1
    else:
        page = int(int(page_offset) / int(page_limit) + 1)
    paginator = Paginator(rrs, page_limit)
    rrs_page = paginator.get_page(page)
    query_result = serializers.serialize('json', rrs_page,
                                         fields=('id', 'city', 'zone_name', 'name', 'type', 'value',
                                                 'disabled_flag', 'reversed_flag', 'user', 'date'))
    result = {}
    # print(query_result)
    # json -> list, get need data
    rrs_count = rrs.count()
    result['total'] = rrs_count
    result['totalNotFilteredField'] = rrs_count
    result['pageNumber'] = page
    result['rows'] = []
    import json
    for rr in json.loads(query_result):
        rr['fields']['id'] = rr['pk']
        rr['fields']['zone'] = rr['fields']['zone_name'] + '.' + rr['fields']['city']
        result['rows'].append(rr['fields'])
    return HttpResponse(json.dumps(result))


def zones(request):
    from .forms import CITY, ZONE
    city = request.GET.get('city', False)
    if city:
        Zone = ZONE[city]
    else:
        Zone = ZONE
    return JsonResponse(Zone, safe=False)


def rr_get(request, id):
    from .models import DnsRrs
    rrs = DnsRrs.objects.using('dns').get(id=id)
    return HttpResponse(rrs.toJSON())


@check_login
@csrf_exempt
def rr_op(request):
    if request.method == 'GET':
        action = request.GET.get('action', '')
        if action == 'add':
            from .forms import addForm
            Form = addForm()
            return render(request, 'initform.html', locals())
        elif action == 'del':
            ids = request.GET.getlist('ids[]', None)
            # print(ids)
            from .models import DnsToolBindrr
            from django.db.models import Q
            DnsToolBindrr.objects.using("dns").filter(Q(id__in=ids)).delete()
            return HttpResponse(1)
        elif action == 'edit':
            from .forms import addForm as editFrom
            id = request.GET.get('id', '')
            Form = editFrom()
            # print(id)
            return render(request, 'initform.html', locals())
        elif action == 'flush':
            return render(request, 'flush.html')
        else:
            return HttpResponse('no Action')


def check_value(value):
    if value.split('.')[-1]: value += '.'
    return value


@csrf_exempt
def rr_add(request):
    if request.method == 'POST':
        from .models import DnsToolBindrr, DnsToolBindzones
        query_zone = DnsToolBindzones.objects.using("dns").filter(type='Forward').values('id', 'city', 'zone_name',
                                                                                         'parent_to').order_by(
            'parent_to')
        zones = {}
        for i in query_zone:
            zones.setdefault(i['city'], {}).setdefault(i['zone_name'], {})
            zones[i['city']][i['zone_name']] = {'id': i['id'], 'parent_to': i['parent_to']}

        import datetime
        name = request.POST.get('name', '')
        type = request.POST.get('type', '')
        value = request.POST.get('value', '')
        city = request.POST.get('city', '')
        zone_name = request.POST.get('zone_name', '')
        cname = request.POST.getlist('cname', '')
        disabled_flag = request.POST.get('disabled_flag', 0)
        if disabled_flag == 'on': disabled_flag = 1
        reversed_flag = request.POST.get('reversed_flag', 0)
        if reversed_flag == 'on': reversed_flag = 1
        user = request.session.get('username','test')
        update_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        # print(name, type, value, city, zone_name, cname, disabled_flag, reversed_flag, user, update_date)
        # print(zones)
        rrs = {}
        if type == 'CNAME': value = check_value(value)
        new_rr = DnsToolBindrr(domain_name=name, type=type, priority=None, value=value, disabled_flag=disabled_flag,
                               reversed_flag=reversed_flag, last_modified_date=update_date, last_modified_user=user,
                               related_to_id=None,
                               zone=DnsToolBindzones.objects.using("dns").get(id=zones[city][zone_name]['id']))
        new_rr.save()
        if zones[city][zone_name]['parent_to']:
            for c in cname:
                zone_parent_name = DnsToolBindzones.objects.using("dns").get(
                    id=zones[city][zone_name]['parent_to']).zone_name
                print(zone_name, zone_parent_name, c)
                cname_value = name + '.' + zone_name
                cname_value = check_value(cname_value)
                new_rr = DnsToolBindrr(domain_name=name, type='CNAME', priority=None, value=cname_value,
                                       disabled_flag=disabled_flag,
                                       reversed_flag=reversed_flag, last_modified_date=update_date,
                                       last_modified_user=user,
                                       related_to_id=None,
                                       zone=DnsToolBindzones.objects.using("dns").get(
                                           id=zones[c][zone_parent_name]['id']))
                new_rr.save()
        else:
            for c in cname:
                if c == city: continue
                zone_parent_name = zone_name
                print(zone_name, zone_parent_name, c)
                cname_value = check_value(value)
                new_rr = DnsToolBindrr(domain_name=name, type='CNAME', priority=None, value=cname_value,
                                       disabled_flag=disabled_flag,
                                       reversed_flag=reversed_flag, last_modified_date=update_date,
                                       last_modified_user=user,
                                       related_to_id=None,
                                       zone=DnsToolBindzones.objects.using("dns").get(
                                           id=zones[c][zone_parent_name]['id']))
                new_rr.save()

        return HttpResponse("Success")


@csrf_exempt
def rr_edit(request, id):
    if request.method == 'POST':
        import datetime

        name = request.POST.get('name', '')
        type = request.POST.get('type', '')
        value = request.POST.get('value', '')
        city = request.POST.get('city', '')
        zone_name = request.POST.get('zone_name', '')
        cname = request.POST.getlist('cname', '')
        disabled_flag = request.POST.get('disabled_flag', 0)
        if disabled_flag == 'on': disabled_flag = 1
        reversed_flag = request.POST.get('reversed_flag', 0)
        if reversed_flag == 'on': reversed_flag = 1
        user = request.session.get('username','test')
        update_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))

        from .models import DnsToolBindrr, DnsToolBindzones, DnsRrs
        old_rr = DnsRrs.objects.using('dns').get(id=id)
        from django.db.models import Q
        # new_rr_zone=DnsToolBindzones.objects.using('dns').filter(Q(city=city) & Q(zone_name=zone_name)).values_list('id')
        # print(name,type,value,city,zone_name,cname,disabled_flag,reversed_flag,user,update_date)
        # DnsToolBindrr.objects.using('dns').filter(id=id).update(domain_name=name,type=type,value=value,last_modified_user=user,last_modified_date=update_date)
        # print(new_rr_zone)
        # new_rr_zone_id=new_rr_zone[0][0]
        # if new_rr_zone_id != old_rr.zone_id:
        #     DnsToolBindrr.objects.using('dns').filter(id=id).update(domain_name=name, type=type, value=value,
        #                                                             zone=new_rr_zone_id,
        #                                                             last_modified_user=user,
        #                                                             last_modified_date=update_date)
        # else:
        DnsToolBindrr.objects.using('dns').filter(id=id).update(domain_name=name, type=type, value=value,
                                                                last_modified_user=user,
                                                                last_modified_date=update_date)
        return HttpResponse("Success")


@check_login
@accept_websocket
def flush_rr(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        import paramiko
        import datetime
        import time
        from io import StringIO
        for message in request.websocket:
            if not message:
                break
            message = message.decode('utf-8')  # 接收前端发来的数据
            if message == 'flush_rr':  # 这里根据web页面获取的值进行对应的操作
                command = 'cd /var/www/dns-tool.base-fx.com/dns_tool/bind_information_manager/ ;python3 flush_db.py'  # 这里是要执行的命令或者脚本
                # command = 'tail -f /tmp/a'  # 这里是要执行的命令或者脚本

                # 远程连接服务器
                hostname = 'int-web01.base-fx.com'
                username = 'root'

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # pky=pkey = paramiko.RSAKey.from_private_key_file('./basefx')
                key_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAr1gRWmXM975JCTgND+GhndZgjF2z4dtuOZC9RStFPdKMwl7o
2NAGuFHYggCQPrOpGHYpLeLlnLtxfdN77lUIrODWdCXlZc+lwhLJ2+uJ1uBBR8AO
wHohUtNMaSxeR7HIJ98vWnzIloTpysq03llSq3RGL3NkiM3Mv0bpRxPojCf4h2wE
9i7yhdfuRQW/scweghNjT2xiptrbm+o3qId2ddfMLXjzN5KgK/h+05Rjre7rSfs5
5SStgJBOvNolLXBlOAhECU6kuoGaXynkh07XDmBggJHZi9zxNd5aJcIGb8rXeJvJ
UV6LfOXEYJq0QfeqkcxZVg36rlqs2fZRljwThQIDAQABAoIBAHonCC/Jq7kLvyXE
/pSJw2WJ60jeHmrBy1AfHTwKoPoorBbct6oTghr2KbanXdXQo4R/DMECyKMfkjju
E/A9HQYSvFO98smylu9U13t141jmcZPioGRGsOBag2jhl+yqVZ4xRXPsanExtw2n
mckswQLgxeRYpzkG5hR6+hiiLec06iBcqZcZx+1lneAH7awJ0frfavmcGjvCLa5p
AXe96skcaeaGJ9Eiu53MeaHpZrCYKT4mJQGd6hc8RjlLTX8V4F/rcL+xx7+hwFfm
DmgyJbKUEAqXNLLMLlSDAalNJ+N1QMtZaVOxBEWY5OfzSBES7OtEboTXkz8kCGFg
8vMtUAECgYEA1fSudRf6bLF/8WMcY77y9iBPtnhuuOLMB/kF+o1DRxvI9TmWqU8d
1t9rGhoGAJXeAw5wwF/PAV/m3Jm5Kou6PbLZtsS5PI86PhpD68qx27g98legTWpr
/JWjKYkQ82tx76ga2sHb9UEos3cd2Gv8IFd04EnZ6U611RRTXvMgbgUCgYEA0cz4
zrEa0zZ1zKyWs0NqJbWBQPPW1xKIhCVjdFJPQCJCloVx+cCQWMtRd6niT7/WoJrp
JolPgZL3mfBuf8EjNIqLFqXdXGiXEmFNSYjMz7VyN3EUAG8hA4O9STbq1/tB3rSA
GSV0Xgj54N2Cgrmdtb/fvS247zMa0ekFeYtgh4ECgYBDZ8W6oCZGLhmXy9i62AKl
ZgKXAxQm7VTIQj0O9Yg3k9pY357GkmVdN5//Zilz78M1BUyiXszRqwwJfeinLcQs
AfezLAELwjfgLtgtJfuotD/X5KFdImUI+3+e607K0ZPgo/5p4t9QQgn3mFRvxX12
Fvd8XefoJ+MDUVb+t+wEnQKBgQC60aDEvOQ8LASdqxnOqzs8NPHR2s/2WCSEN57m
F91GKLvOuSmS0iw3RWVX/0js5tDB1u/CRwcrRKmCxJxA2sT0pmHQWwZQoTnVPhvK
XSyz0MjSIblD4bEuJgNJzMM2bCBtpaFjwvxqN+f6moT6zzpme2NKXAqPxZweSzd6
0ee1AQKBgEct3uiUM/+Ezc7lPLkL/mueJsIkS2beaMHhNa6EsDfhmQdx/pLNkZ2Y
7EUf9ve3u33ScceIMNSOYfnbPkcLeJC9cIVDaBl1kYknn41vBbMNl46te1TlzpMr
sIJuvCNtlDJhg4lGR/VQ9WmFIye0aAASX87XsWWw0BfXKGl0lmPF
-----END RSA PRIVATE KEY-----"""
                pkey = paramiko.RSAKey(file_obj=StringIO(key_str))
                ssh.connect(hostname=hostname, username=username, pkey=pkey)
                chan = ssh.invoke_shell()
                chan.settimeout(30)
                chan.send(command + '\n')
                space_count = 0

                # dt=datetime.datetime.now()
                # f=open(dt.strftime("%Y%m%d-%H%M%S"),'w+')
                while True:
                    chan.send(" ")
                    result = chan.recv(4096).decode()
                    # print(result)
                    if len(result) == 1:
                        time.sleep(1)
                        space_count += 1
                    else:
                        space_count = 0
                        # f.writelines(result.strip())
                        request.websocket.send(result.strip())  # 发送消息到客户端
                    if space_count > 10:
                        break
                # f.close()
                chan.close()
                ssh.close()  # 关闭ssh连接
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))
