# Generated by Django 3.0.8 on 2020-08-08 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0009_auto_20200803_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
