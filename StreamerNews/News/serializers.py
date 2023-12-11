from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from rest_framework.serializers import ModelSerializer

from News.models import News


class NewsSerializer(ModelSerializer):
    # author = ReadOnlyField(source="get_author")
    # author = ReadOnlyField(source="author.username")
    category = ReadOnlyField(source="category.title")
    # fullname = ReadOnlyField(source="get_author")
    fullname = serializers.CharField(max_length=100, read_only=True)
    readers = ReadOnlyField(source="get_readers")
    readers_count = serializers.IntegerField(read_only=True)
    like = serializers.BooleanField()

    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'readers', 'img', 'author',
                  'fullname', 'readers_count', 'like']
