# Generated by Django 4.2.16 on 2024-10-08 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_remove_article_image_url_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="image_url",
            field=models.URLField(blank=True),
        ),
    ]