# Generated by Django 3.0.8 on 2020-07-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_feed_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='image',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/'),
        ),
    ]
