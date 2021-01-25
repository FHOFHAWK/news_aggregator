from django.urls import path


from news.views import save_news


urlpatterns = [
    path('save-news', save_news)
]
