# Generated by Django 4.2.5 on 2023-10-08 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_fitnessservice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnessservice',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='fitnessservice',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='fitnessservice',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]