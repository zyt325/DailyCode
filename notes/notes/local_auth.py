from django.contrib.auth import authenticate,login
from django.shortcuts import redirect,HttpResponse

def check_auth(func):
    def warpper(request,*args,**kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect("/accounts/login")
    return warpper


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['is_login'] = True
            request.session['username'] = username
            return redirect('/')
        else:
            return HttpResponse("账户或密码错误")
    else:
        return redirect('/accounts/login')