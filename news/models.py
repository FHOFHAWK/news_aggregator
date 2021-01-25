from django.db import models


class NewsItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title
