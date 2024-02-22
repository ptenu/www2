# Generated by Django 5.0.2 on 2024-02-18 21:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newspost",
            name="created_at",
            field=models.DateField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Post created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="newspost",
            name="updated_at",
            field=models.DateField(auto_now=True, verbose_name="Post updated at"),
        ),
    ]
