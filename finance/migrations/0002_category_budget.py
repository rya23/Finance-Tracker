# Generated by Django 5.0.6 on 2024-05-21 19:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="budget",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
