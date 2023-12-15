from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Exists, OuterRef


class NewsQuerySet(models.QuerySet):
    def with_readers_count(self):
        return self.annotate(
            readers_count=Count('readers')
        )

    def with_is_like(self, user):
        return self.annotate(
            like=(
                Exists(UserNewsRelation.objects.filter(user=user,
                                                       news=OuterRef("pk")))
            )
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    readers = models.ManyToManyField(User, through='UserNewsRelation',
                                     related_name='news')
    img = models.ImageField(upload_to='news', null=True, blank=True,
                            verbose_name='Изображение')
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = NewsQuerySet.as_manager()

    @property
    def get_readers(self):
        return [reader.username for reader in self.readers.all()]

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"
        ordering = ('-date_created',)

    def __str__(self):
        return f'{self.author} : {self.title} {self.date_created}'


# Create your models here.
class UserNewsRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User-news Relation"
        verbose_name_plural = "User-news Relation"

    def __str__(self):
        return f'{self.news.title}:{self.user.username}'
