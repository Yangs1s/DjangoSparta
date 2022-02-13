# Generated by Django 4.0 on 2022-02-13 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabom', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('user', 'article'), name='unique_user_article'),
        ),
    ]
