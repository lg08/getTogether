# Generated by Django 3.1.7 on 2021-04-28 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_auto_20210428_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_event',
        ),
        migrations.AddField(
            model_name='post',
            name='is_event',
            field=models.BooleanField(default=False),
        ),
    ]