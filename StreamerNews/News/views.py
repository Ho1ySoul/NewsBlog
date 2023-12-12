from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from News.models import News
from News.serializers import NewsSerializer

import logging


logger = logging.getLogger('main')


class NewsViewSet(ModelViewSet):
    queryset = (
        News.objects
        .prefetch_related('readers')
        .select_related("category", "author")
        .get_readers_count()
        .with_author_full_name()
        .get_is_like()
        # TODO: удали лишние строки кода
        # .annotate(
        #     fullname=Concat(
        #         'author__first_name',
        #         'author__last_name'
        #     ),
        #     readers_count=Count('readers'),
        #     like=Exists(UserNewsRelation.objects.filter(news=OuterRef('pk')))
        #
        # )
    )

    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category',
                        'author']  # поиск по одному полю
    ordering_fields = ['title']

    search_fields = [
        'title',
        'content',
        'fullname'
    ]  # поиск по двум полям сразу

    def perform_create(self, serializer):
        logger.info("ЭТО ОНО")
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    # permission_classes = [IsAuthenticatedOrReadOnly]
    #
    # def get(self, request, format=None):
    #     return Response()
