# Generated by Django 3.1.7 on 2021-04-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_merge_20210427_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_event',
            field=models.BooleanField(default=False),
        ),
    ]
