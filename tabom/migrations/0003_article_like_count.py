# Generated by Django 4.0 on 2022-02-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tabom", "0002_like_unique_user_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="like_count",
            field=models.IntegerField(default=0),
        ),
    ]
