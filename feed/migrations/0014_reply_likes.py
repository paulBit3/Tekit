# Generated by Django 3.0.8 on 2020-08-11 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200811_1312'),
        ('feed', '0013_auto_20200810_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='r_likes', to='accounts.UserProfile'),
        ),
    ]
