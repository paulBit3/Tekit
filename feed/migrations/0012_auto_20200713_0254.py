# Generated by Django 3.0.8 on 2020-07-13 07:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0011_auto_20200710_0158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(null=True, validators=[django.core.validators.MinLengthValidator(150)]),
        ),
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='like',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='feed.Comment'),
        ),
        migrations.AddField(
            model_name='like',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='like',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='feed.Topic'),
        ),
        migrations.AddField(
            model_name='like',
            name='value',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Feed'),
        ),
        migrations.RemoveField(
            model_name='feed',
            name='likes',
        ),
        migrations.AddField(
            model_name='feed',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='like',
            name='feed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feeds', to='feed.Feed'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'topic', 'feed', 'comment', 'value')},
        ),
        migrations.RemoveField(
            model_name='like',
            name='created_on',
        ),
    ]