# Generated by Django 4.2.16 on 2024-12-10 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finalproject', '0004_discount_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finalproject.category'),
        ),
        migrations.AddField(
            model_name='discount',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
