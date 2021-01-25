from django.contrib import admin
from django.urls import path, include

from news.views import PostsViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', PostsViewSet.as_view()),
    path('', include('news.urls')),
]
