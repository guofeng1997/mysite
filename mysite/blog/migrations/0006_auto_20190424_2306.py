# Generated by Django 2.1 on 2019-04-24 15:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190424_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 24, 15, 6, 7, 163726, tzinfo=utc)),
        ),
    ]
