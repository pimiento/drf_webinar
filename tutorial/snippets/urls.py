from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from django.contrib import admin

from snippets import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url('mysnips', views.SnippetsListUser.as_view()),
    re_path(r'^snipskwargs/(?P<username>.+)/$', views.SnippetsListUserKwargs.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    path('simplesnips', views.ListSnippets.as_view()),
]
