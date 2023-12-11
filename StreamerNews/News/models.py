from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Exists, OuterRef
from django.db.models.functions import Concat


class NewsQuerySet(models.QuerySet):
    def get_author_fullname(self):
        # TODO: Имя метода не информативно, из него ожидаю, что метод
        #  возвращает стоку с полным именем автора. В этих методах часто
        #  используют имена with_foo, annotate_foo ...,
        #  например with_author_full_name
        return self.annotate(
            fullname=Concat(
                'author__first_name',
                'author__last_name'
            ))

    def get_readers_count(self):
        # TODO: аналогично
        return self.annotate(
            readers_count=Count('readers'))

    def get_is_like(self):
        # TODO: и тут
        return self.annotate(
            like=Exists(UserNewsRelation
                        .objects
                        .filter(news=OuterRef('pk')))
        )


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='my_post')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    readers = models.ManyToManyField(User, through='UserNewsRelation',
                                     related_name='news')
    img = models.ImageField(upload_to='news', null=True, blank=True,
                            verbose_name='Изображение')

    objects = NewsQuerySet.as_manager()

    # @property
    # def get_author(self):
    #     author1 = self.author.first_name + self.author.last_name
    #     return author1

    @property
    def get_readers(self):
        return [reader.username for reader in self.readers.all()]

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        #TODO: сюда стоит добавить сортировку

    def __str__(self):
        return self.title


# Create your models here.
class UserNewsRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.news.title

    # TODO: добавь Meta
