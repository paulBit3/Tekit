# Generated by Django 3.0.8 on 2020-07-09 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_delete_topicmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, upload_to='topicphotos/%Y/%m/%d/'),
        ),
    ]