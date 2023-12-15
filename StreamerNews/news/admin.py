from django.contrib import admin

from news.models import Category, News, UserNewsRelation


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'content', 'category', 'img', 'date_created',
              'is_active']
    readonly_fields = ['author', 'is_active', 'date_created']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(UserNewsRelation)
class UserNewsRelationAdmin(admin.ModelAdmin):
    fields = ['user', 'news', 'like']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title']
