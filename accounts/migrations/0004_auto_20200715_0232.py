# Generated by Django 3.0.8 on 2020-07-15 07:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20200713_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='photo',
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile_pic'),
        ),
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='RelationshipRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2020, 7, 15, 2, 32, 8, 348341), verbose_name='created at')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationship_request_set1', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationship_request_set2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2020, 7, 15, 2, 32, 8, 348341), verbose_name='created_at')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationship_set1', to=settings.AUTH_USER_MODEL)),
                ('relationship_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.RelationshipType')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationship_set2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
