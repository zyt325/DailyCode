from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from notes.local_auth import check_auth


# Create your views here.

# get classes about article
def list_classes():
    from . import models
    classes = models.ZytArticleclass.objects.using('notes').all()
    article_classes = {}
    for i in classes:
        if i.upper_class == 0:
            if not article_classes.get(i.id):
                article_classes.setdefault(i.id, {}).setdefault('info', i)
            else:
                article_classes[i.id]['info'] = i
        elif i.upper_class != 0:
            if article_classes.get(i.upper_class):
                article_classes[i.upper_class].setdefault('sub', []).append(i)
            else:
                article_classes.setdefault(
                    i.upper_class, {}).setdefault('info', '')
                article_classes[i.upper_class].setdefault('sub', []).append(i)
    return article_classes


@check_auth
def index(request):
    from . import models
    title = 'Article List'
    article_classes = list_classes()

    from django.core.paginator import Paginator
    class_id = request.GET.get('class_id', '-1')
    if class_id and class_id != '-1':
        from django.db.models import Q
        article_set = models.ZytArticleView.objects.using('notes').filter(
            Q(class_id=class_id) | Q(upper_class=class_id)).values('article_id', 'class_id', 'file_name',
                                                                   'article_name', 'upper_class').order_by(
            "article_name")
    else:
        article_set = models.ZytArticleView.objects.using('notes').values('article_id', 'class_id', 'file_name',
                                                                          'article_name').order_by("article_name")
    paginator = Paginator(article_set, 15)
    page = request.GET.get('page', 1)
    articles = paginator.get_page(page)
    return render(request, 'notes.html', context=locals())


# @check_auth
@csrf_exempt
def add_article(request):
    if request.method == 'GET':
        title = 'Article ADD'
        article_classes = list_classes()
        return render(request, 'add.html', context=locals())
    elif request.method == 'POST':
        from . import models
        from django.utils.timezone import now
        article_title = request.POST.get("title", '')
        class_id = request.POST.get('class_id', '')
        article_body = request.POST.get('body', '')
        article_body_html = request.POST.get('body_html', '')
        secret = request.POST.get('secret', '')
        filename_rand = "doc_%s.html" % genera_uuid()
        create_date = now()
        if secret != "325":
            return HttpResponse(3)
        if len(models.NoteArticle.objects.filter(title=article_title)) != 0:
            return HttpResponse(2)
        try:
            article_ex = models.NoteArticle(title=article_title, body=article_body, file_name=filename_rand,
                                            create_at=create_date,
                                            category=models.NoteCategory.objects.get(id=class_id))
            article_ex.save()
            save_article(filename_rand, article_title,
                         article_ex.id, class_id, article_body_html)
            return JsonResponse({'status': 1, 'result': {'filename': filename_rand}})
        except Exception as e:
            print(e)
            return HttpResponse(4)


# @check_auth
@csrf_exempt
def edit_article(request):
    if request.method == 'GET':
        title = 'Article Edit'
        article_classes = list_classes()
        class_id = int(request.GET.get('class_id'))
        return render(request, 'edit.html', context=locals())
    elif request.method == 'POST':
        from . import models
        from django.utils.timezone import now
        from django.db.models import Q
        article_id = int(request.POST.get("article_id", ''))
        article_title = request.POST.get("title", '')
        class_id = request.POST.get('class_id', '')
        article_body = request.POST.get('body', '')
        article_body_html = request.POST.get('body_html', '')
        secret = request.POST.get('secret', '')
        filename_rand = models.NoteArticle.objects.filter(id=article_id)[
            0].file_name
        create_date = now()
        if secret != "325":
            return HttpResponse(3)
        if len(models.NoteArticle.objects.filter(
                Q(title=article_title) & ~Q(id=article_id))) > 0:
                return HttpResponse(2)
        try:
            article_ex = models.NoteArticle.objects.get(id=article_id)
            article_ex.title = article_title
            article_ex.body = article_body
            article_ex.create_at = create_date
            article_ex.category = models.NoteCategory.objects.get(id=class_id)
            article_ex.save()
            save_article(filename_rand, article_title,
                         article_id, class_id, article_body_html)
            return JsonResponse({'status': 1, 'result': {'filename': filename_rand}})
        except Exception as e:
            print(e)
            return HttpResponse(4)


def del_article(request):
    pass


def list_article(request):
    from django.core.paginator import Paginator
    from django.core import serializers
    from . import models
    class_id = request.GET.get('class_id', '-1')
    search_word = request.GET.get('search_word', '')
    if search_word:
        from django.db.models import Q
        article_set = models.ZytArticleView.objects.filter(
            Q(body__icontains=search_word) | Q(article_name__icontains=search_word)).order_by("article_name")
    elif class_id and class_id != '-1':
        from django.db.models import Q
        article_set = models.ZytArticleView.objects.using('notes').filter(
            Q(class_id=class_id) | Q(upper_class=class_id)).order_by("article_name")
    else:
        article_set = models.ZytArticleView.objects.using(
            'notes').all().order_by("article_name")
    paginator = Paginator(article_set, 15)
    page = request.GET.get('page', 1)
    articles = paginator.get_page(page)
    result = {}
    result['search_word'] = search_word
    result['class_id'] = class_id
    if articles.paginator.num_pages != 1:
        if articles.has_previous() and articles.has_next():
            result['page'] = {"cur_page": articles.number, "num_pages": articles.paginator.num_pages,
                              "prev_page": articles.previous_page_number(),
                              "next_page": articles.next_page_number()}
        elif articles.has_previous() and not articles.has_next():
            result['page'] = {"cur_page": articles.number, "num_pages": articles.paginator.num_pages,
                              "prev_page": articles.previous_page_number()}
        else:
            result['page'] = {"cur_page": articles.number, "num_pages": articles.paginator.num_pages,
                              "next_page": articles.next_page_number()}
    result['data'] = serializers.serialize('json', articles,
                                           fields=('article_id', 'class_id', 'file_name', 'article_name'))
    return JsonResponse(result)
    # return HttpResponse(serializers.serialize('json', articles,fields=('article_id', 'class_id', 'file_name', 'article_name')))


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        import os
        from django.conf import settings
        upload_path = settings.MEDIA_ROOT + '/uploads/'
        upload_url = settings.MEDIA_URL + 'uploads/'
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        # request.FILES  < MultiValueDict: {'editormd-image-file': [ < InMemoryUploadedFile: gpo - filter01.png(image / png) >]} >
        imgs = request.FILES.getlist('editormd-image-file')
        # print(imgs)
        # print(type(imgs))
        for img in imgs:
            # print(img)
            imgPath = upload_path + img.name
            imgUrl = upload_url + img.name
            # print(imgPath)
            with open(imgPath.encode('utf-8'), 'wb') as f_img:
                for i in img.chunks():
                    f_img.write(i)
    return JsonResponse({'success': 1, 'message': "上传成功", 'url': imgUrl})


def genera_uuid():
    from uuid import uuid4
    uuidChars = ("a", "b", "c", "d", "e", "f",
                 "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                 "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
                 "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
                 "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                 "W", "X", "Y", "Z")

    def short_uuid():
        uuid = str(uuid4()).replace('-', '')
        result = ''
        for i in range(0, 8):
            sub = uuid[i * 4: i * 4 + 4]
            x = int(sub, 16)
            result += uuidChars[x % 0x3E]
        return result

    return short_uuid()


def save_article(filename, title, article_id, class_id, body_html):
    article_body_html_content = """<!DOCTYPE html>
  <html lang="zh">
  <head>
    <meta charset="utf-8" />
    <title>{0}</title>
    <link rel="stylesheet" href="/static/css/article.css" />
  </head>
  <body>
  <div id="container">
  <div id="article_header">
      <header>
        <span><button article_id="{1}" class_id="{2}" onclick="article_edit(this)">Edit</button></span>
      </header>
    </div>
    <div id="article_sort">
    </div>
    <div id="article_list" class="markdown-body editormd-preview-container" previewcontainer="true">
      {3}
  </div>
  <script src="/static/js/article.js"></script>
  </body>
  </html>
    """.format(title, article_id, class_id, body_html)
    from django.conf import settings
    import os
    upload_path = settings.MEDIA_ROOT + '/articles/'
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    article_path = upload_path + filename
    with open(article_path, 'wb') as f:
        f.write(article_body_html_content.encode("utf-8"))


def get_article(request):
    from . import models
    article_results = models.ZytArticleView.objects.filter(
        article_id=request.GET.get('id', ''))
    result = {}
    if len(article_results) > 0:
        result['body'] = str(article_results[0].body, encoding='utf-8')
        result['title'] = article_results[0].article_name
    return JsonResponse(result)


def v2(request):
    title = 'Article List'
    article_classes = list_classes()
    return render(request, 'v2_notes.html', context=locals())
