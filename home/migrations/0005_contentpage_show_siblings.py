# Generated by Django 5.0.2 on 2024-02-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_contentpage_remove_homepage_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="contentpage",
            name="show_siblings",
            field=models.BooleanField(default=False),
        ),
    ]
