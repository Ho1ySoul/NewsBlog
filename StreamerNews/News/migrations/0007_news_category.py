# Generated by Django 5.0 on 2023-12-07 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('News', '0006_category_remove_news_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.ForeignKey(default=1,
                                    on_delete=django
                                    .db
                                    .models
                                    .deletion
                                    .CASCADE,
                                    to='News.category'),
        ),
    ]
