# Generated by Django 4.2.5 on 2023-10-08 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_fitnessservice_options_fitnessservice_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnessservice',
            name='contact_data',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]