from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token, api_settings
from rest_framework.documentation import include_docs_urls

from . import note_views, tools_views

router = routers.DefaultRouter()
router.register(r'note_theme', note_views.ThemeViewSet, basename='note_theme')
router.register(r'note_category_article', note_views.Category_ArticleViewSet, basename='note_category_article')
router.register(r'note_categorys', note_views.CategorysViewSet, basename='note_categorys')
router.register(r'note_category', note_views.CategoryViewSet, basename='note_category')
router.register(r'note_articles', note_views.ArticlesViewSet, basename='note_articles')
router.register(r'note_article', note_views.ArticleViewSet, basename='note_article')

router.register(r'tool_category', tools_views.ToolsCategoryViewSet, basename='tool_category')
router.register(r'tool_url', tools_views.ToolsUrlViewSet, basename='tool_url')
router.register(r'tool_view', tools_views.ToolsViewViewSet, basename='tool_view')
router.register(r'tool_categorys', tools_views.CategoryViewSet, basename='tool_categorys')
router.register(r'tool_urls', tools_views.UrlsViewSet, basename='tool_urls')


# router.register('^test/(?P<category>.+)/$', tools_views.ToolsUrlbyCategoryList.as_view(),basename='test'),

# manual token
from django.contrib.auth import authenticate
from notes.aes import EncDecAES
from django.http import JsonResponse

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def manual_token(request):
    if request.method == 'POST':
        import json
        postBody = json.loads(request.body)
        username = postBody.get('username', '')
        password = postBody.get('password', '')
        credentials = {
            'username': username,
            'password': (EncDecAES().decrypt(password, 'tools')).decode()
        }
        user = authenticate(**credentials)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return JsonResponse({'token': token})


urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='docs')),
    path('token-manual/', manual_token),
    path('token-auth/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
]
