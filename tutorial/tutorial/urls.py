from django.conf.urls import include, url
from rest_framework.schemas import get_schema_view
from rest_framework.authtoken import views

API_TITLE = 'Pastebin API'
API_DESCRIPTION = 'A Web API for creating and viewing highlighted code snippets.'
schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    url(r'^v1/', include('snippets.urls')),
    url(r'^v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/api-token-auth/', views.obtain_auth_token)
]
