# Generated by Django 4.2.5 on 2023-10-07 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_remove_comment_parent_comment_reply'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reply',
        ),
    ]