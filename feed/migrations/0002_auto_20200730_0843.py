# Generated by Django 3.0.8 on 2020-07-30 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicaction',
            name='image',
            field=models.ImageField(upload_to='topimages/'),
        ),
    ]
