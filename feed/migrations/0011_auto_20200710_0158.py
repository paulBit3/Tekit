# Generated by Django 3.0.8 on 2020-07-10 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0010_auto_20200709_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.ImageField(default='images/topicholder.png', upload_to='topimages/'),
        ),
    ]
