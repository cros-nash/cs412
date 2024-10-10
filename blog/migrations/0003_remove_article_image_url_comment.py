# Generated by Django 4.2.16 on 2024-10-08 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_article_image_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="image_url",
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("author", models.TextField()),
                ("text", models.TextField()),
                ("published", models.DateTimeField(auto_now=True)),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.article"
                    ),
                ),
            ],
        ),
    ]
