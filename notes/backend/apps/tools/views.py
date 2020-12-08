from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.db.models import Q, Count


def index(request):
    from . import models
    # urls_set = models.Urls.objects.using('tools').all().order_by('class_field')
    class_set = models.ToolsCategory.objects.using('tools').all()
    titlce = 'Url List'
    return render(request, 'tools.html', locals())
