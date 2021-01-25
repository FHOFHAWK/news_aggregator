from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from celery import shared_task

from news.models import NewsItem
from news.serializers import NewsItemSerializer

url = 'https://news.ycombinator.com/'

allowed_url_params = ['order', 'offset', 'limit']
allowed_order_params = ['id', 'title', 'url', 'created']


@shared_task
def save_news(request):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    limit = 30
    news = soup.findAll('a', class_='storylink', limit=limit)

    for new_item in news:
        href = new_item.get('href')
        text = new_item.text
        try:
            if href.startswith('http') and not NewsItem.objects.get(title=text):
                NewsItem.objects.create(title=text, url=href)
        except NewsItem.DoesNotExist:
            NewsItem.objects.create(title=text, url=href)
    return HttpResponse(f'Было сохранено {limit} новостей с {url}.')


class PostsViewSet(ListAPIView):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer()

    def get(self, request, *args, **kwargs):
        if isinstance(calculate_url_params(request.GET), HttpResponse):
            return calculate_url_params(request.GET)
        else:
            order, offset, limit = calculate_url_params(request.GET)

        queryset = self.get_queryset()

        if order:
            queryset = queryset.order_by(order)

        if offset != -1:
            queryset = queryset[offset:]

        if limit != -1:
            queryset = queryset[:limit]

        serializer = NewsItemSerializer(queryset, many=True)
        return Response(serializer.data)


def calculate_url_params(request_get_dict):
    order = None
    offset = -1
    limit = 5
    for item in list(request_get_dict.keys()):
        if item in allowed_url_params:

            if item == 'order':
                order = request_get_dict.get(item, None)
                if order and isinstance(order, str) and order in allowed_order_params:
                    pass
                else:
                    return HttpResponse(f'Неверный атрибут {order} параметра {item}.')

            if item == 'offset' or item == 'limit':
                try:
                    value = int(request_get_dict.get(item, -1))
                    if item == 'offset':
                        offset = value
                    elif item == 'limit':
                        limit = value
                except ValueError:
                    return HttpResponse(f'Атрибут параметра {item} должен быть числом.')

                if 0 <= value < NewsItem.objects.count():
                    pass
                else:
                    return HttpResponse(f'Неверный атрибут {value} параметра {item}.')

        else:
            return HttpResponse(f'Передан неверный параметр {item}.')
    return order, offset, limit
