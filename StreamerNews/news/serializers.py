from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from streamer_news.settings import DATETIME_FORMAT

from .models import Category, News


class UserSerializer(ModelSerializer):
    fullname = ReadOnlyField(source="get_full_name")

    class Meta:
        model = User
        fields = ['id', 'fullname']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class CategoryPostSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class NewsSerializer(ModelSerializer):
    fullname = serializers.CharField(max_length=100, read_only=True)
    readers = ReadOnlyField(source="get_readers")
    readers_count = serializers.IntegerField(read_only=True)
    like = serializers.BooleanField(read_only=True)
    date_created = serializers.DateTimeField(format=DATETIME_FORMAT,
                                             read_only=True)

    author = UserSerializer(read_only=True)

    category = CategorySerializer()

    class Meta:
        model = News
        fields = ['title',
                  'content',
                  'category',
                  'readers',
                  'img',
                  'author',
                  'readers_count',
                  'fullname',
                  'is_active',
                  'date_created',
                  'like',
                  ]


class NewsPostSerializer(NewsSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    def create(self, validated_data):
        return News.objects.create(**validated_data)
        # def create(self, validated_data):
        #     print(validated_data)
        #     category_id = validated_data.pop('category')
        #
        #     category = Category.objects.get(pk=category_id['title'])
        #
        #     return news.objects.create(category=category, **validated_data)
