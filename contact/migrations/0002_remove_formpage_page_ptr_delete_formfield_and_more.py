# Generated by Django 5.0.2 on 2024-02-19 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="formpage",
            name="page_ptr",
        ),
        migrations.DeleteModel(
            name="FormField",
        ),
        migrations.DeleteModel(
            name="FormPage",
        ),
    ]