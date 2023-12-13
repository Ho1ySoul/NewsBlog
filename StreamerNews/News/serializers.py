from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from rest_framework.serializers import ModelSerializer

from News.models import News, Category
from StreamerNews.settings import DATETIME_FORMAT


class UserSerializer(ModelSerializer):
    fullname = ReadOnlyField(source="get_full_name")

    class Meta:
        model = User
        fields = ['id', 'fullname']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class NewsSerializer(ModelSerializer):
    fullname = serializers.CharField(max_length=100, read_only=True)
    readers = ReadOnlyField(source="get_readers")
    readers_count = serializers.IntegerField(read_only=True)
    like = serializers.BooleanField(default=False)
    date_created = serializers.DateTimeField(format=DATETIME_FORMAT)

    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

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
