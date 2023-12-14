from django.contrib.sites import requests
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import status

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from News.models import News, Category
from News.permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly
from News.serializers import NewsSerializer, CategorySerializer, CategoryPostSerializer, NewsPostSerializer

import logging

logger = logging.getLogger('main')





class NewsViewSet(ModelViewSet):
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
            return (self.queryset
                    .prefetch_related('readers')
                    .select_related("category", "author")
                    .with_readers_count()
                    .with_author_full_name()
                    .with_is_like(self.request.user)

                    )
        else:
            return (self.queryset
                    .prefetch_related('readers')
                    .select_related("category", "author")
                    .with_readers_count()
                    .with_author_full_name()

                    )

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return NewsPostSerializer
        else:
            return NewsSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        logger.info("ЭТО ОНО")
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return CategoryPostSerializer
        else:
            return CategorySerializer
