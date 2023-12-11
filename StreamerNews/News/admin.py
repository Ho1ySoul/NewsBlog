from django.contrib import admin
from News.models import News, UserNewsRelation, Category


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'content', 'category', 'img', 'date_created',
              'is_active']
    readonly_fields = ['author', 'is_active','date_created']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

# TODO: Для чего тут pass?
    pass


@admin.register(UserNewsRelation)
class UserNewsRelationAdmin(admin.ModelAdmin):
    fields = ['user', 'news', 'like']
    # readonly_fields = ['like']
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title']
    pass
