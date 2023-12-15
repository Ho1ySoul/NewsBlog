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
    readers = ReadOnlyField(source="get_readers")
    readers_count = serializers.IntegerField(read_only=True)
    like = serializers.BooleanField(read_only=True)
    date_created = serializers.DateTimeField(format=DATETIME_FORMAT,
                                             read_only=True)

    author = UserSerializer(read_only=True)
    fullname = ReadOnlyField(source='author.fullname')
    category = CategorySerializer()

    class Meta:
        model = News
        fields = [
            'title',
            'content',
            'category',
            'readers',
            'img',
            'author',
            'fullname',
            'readers_count',
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
