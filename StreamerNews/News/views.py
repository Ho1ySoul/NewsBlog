from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from News.models import News, Category
from News.serializers import NewsSerializer, CategorySerializer

import logging


logger = logging.getLogger('main')


class NewsViewSet(ModelViewSet):
    queryset = (
        News.objects
        .prefetch_related('readers')
        .select_related("category", "author")
        .with_readers_count()
        .with_author_full_name()
        .with_is_like()
    )

    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category',
                        'author']
    ordering_fields = ['title']

    search_fields = [
        'title',
        'content',
        'fullname'
    ]

    def perform_create(self, serializer):
        logger.info("ЭТО ОНО")
        serializer.validated_data['author'] = self.request.user
        serializer.save()

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()