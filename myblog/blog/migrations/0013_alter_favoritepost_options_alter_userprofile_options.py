# Generated by Django 4.2.5 on 2023-10-05 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_post_author_favoritepost_post_favorited_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritepost',
            options={'verbose_name': 'Избранный пост', 'verbose_name_plural': 'Избранные посты'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профиль пользователя', 'verbose_name_plural': 'Профили пользователей'},
        ),
    ]
