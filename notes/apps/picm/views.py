from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import Single_UploadFileForm, Mult_UploadFileForm


def index(request):
    return render(request, 'index.html')


def handle_uploaded_file(f):
    import os
    from django.conf import settings
    upload_root = settings.PICM_ROOT
    upload_url = settings.MEDIA_URL + 'picm/' + "%s" % f.name
    upload_path = "%s%s" % (upload_root, f.name)
    try:
        if os.path.isfile(upload_path): return {'status': 'False', 'desc': '存储中图片名称重复', 'path': upload_url}
        with open(upload_path.encode('utf-8'), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except FileNotFoundError:
        pass
    except Exception as e:
        return {'status': 'False', 'desc': "上传失败%s" % e, 'path': upload_url}

    return {'status': 'True', 'desc': '上传成功', 'path': upload_url}


def single_upload(request):
    if request.method == 'POST':
        form = Single_UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['File'])
            return HttpResponseRedirect('/picm/single_upload/')
    else:
        form = Single_UploadFileForm()
    return render(request, 'single_upload_images.html', {'form': form})


def mult_upload(request):
    if request.method == 'POST':
        form = Mult_UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('Files')
            print(files)
            for f in files:
                handle_uploaded_file(f)
            return HttpResponseRedirect('/picm/mult_upload/')
    else:
        form = Mult_UploadFileForm()
    return render(request, 'mult_upload_images.html', {'form': form})


def vue_upload(request):
    if request.method == 'POST':
        pwd = request.POST.get('pwd', '')
        cat_id = request.POST.get('category_id', -1)
        print(cat_id)
        if pwd != '325':
            return JsonResponse({'status': 'False', 'desc': '密钥错误'})
        # form = Mult_UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        files = request.FILES.getlist('file')
        for f in files:
            from . import models
            # print(f)
            try:
                models.PicmPath.objects.using('picm').get(name=f.name)
                return JsonResponse({'status': 'False', 'desc': '数据库中图片名称重复'})
            except ObjectDoesNotExist:
                pass

            result = handle_uploaded_file(f)
            if result['status']:
                print(cat_id)
                pcategory = models.PicmCategory(id=cat_id)
                print(pcategory)
                ppath = models.PicmPath()
                ppath.name = f.name
                ppath.category = pcategory
                ppath.save()
            return JsonResponse(result)
    else:
        return JsonResponse({'status': 'False', 'desc': '使用POST'})
