# Generated by Django 3.1.7 on 2021-04-24 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_event'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
    ]