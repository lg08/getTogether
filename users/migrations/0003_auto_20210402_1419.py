# Generated by Django 3.1.7 on 2021-04-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210322_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default='put JSONobject here', max_length=50000),
        ),
    ]
