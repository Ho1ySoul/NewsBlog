from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from rest_framework.serializers import ModelSerializer

from News.models import News
from StreamerNews.settings import DATETIME_FORMAT


class NewsSerializer(ModelSerializer):
    category = ReadOnlyField(source="category.title")
    fullname = serializers.CharField(max_length=100, read_only=True)
    readers = ReadOnlyField(source="get_readers")
    readers_count = serializers.IntegerField(read_only=True)
    like = serializers.BooleanField()
    date_created = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = News
        fields = ['title',
                  'content',
                  'category',
                  'readers',
                  'img',
                  'author',
                  'fullname',
                  'readers_count',
                  'like',
                  'fullname',
                  'readers_count',
                  'like',
                  'is_active',
                  'date_created'
                  ]
