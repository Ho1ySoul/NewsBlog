import logging

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Category, News
from .permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from .serializers import (CategoryPostSerializer, CategorySerializer,
                          NewsPostSerializer, NewsSerializer)


class NewsViewSet(ModelViewSet):
    logger = logging.getLogger('main')
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category',
                        'author']
    ordering_fields = ['title']

    search_fields = [
        'title',
        'content',
        'fullname'
    ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (
                self.queryset
                .prefetch_related('readers')
                .select_related("category", "author")
                .with_readers_count()
                .with_is_like(self.request.user)
            )

        return (
            self.queryset
            .prefetch_related('readers')
            .select_related("category", "author")
            .with_readers_count()
        )

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return NewsPostSerializer

        return NewsSerializer

    def perform_create(self, serializer):
        self.logger.info("ЭТО ОНО")
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return CategoryPostSerializer

        return CategorySerializer
