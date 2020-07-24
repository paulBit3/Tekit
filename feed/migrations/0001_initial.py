# Generated by Django 3.0.8 on 2020-07-23 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopicAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(default='images/topicholder.png', upload_to='topimages/')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(blank=True)),
                ('read_time', models.PositiveSmallIntegerField(default=0, verbose_name='View Time')),
                ('hot_topics', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.TopicAction')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-hot_topics'],
            },
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='accounts.UserProfile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=160)),
                ('image', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('status', models.IntegerField(choices=[(1, 'new'), (2, 'verified'), (3, 'published')], default=1)),
                ('is_read', models.BooleanField(blank=True)),
                ('read_time', models.PositiveSmallIntegerField(default=0, verbose_name='View Time')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile')),
                ('likes', models.ManyToManyField(blank=True, related_name='feed_likes', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Topic')),
                ('view_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feeds', to='accounts.UserProfile')),
            ],
            options={
                'verbose_name_plural': 'feeds',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=160)),
                ('is_read', models.BooleanField(blank=True)),
                ('read_time', models.PositiveSmallIntegerField(default=0, verbose_name='Read Time')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented', to='accounts.UserProfile')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='feed.Feed')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to='accounts.UserProfile')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='feed.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('view_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed', to='accounts.UserProfile', verbose_name='View')),
            ],
        ),
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')], default=1, verbose_name='likes')),
                ('date', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes_comment', to='feed.Comment')),
                ('feed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes_feed', to='feed.Feed')),
                ('liked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='accounts.UserProfile')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('feed', 'comment', 'liked_by')},
            },
        ),
    ]
