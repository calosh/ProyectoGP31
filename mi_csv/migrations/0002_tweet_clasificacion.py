# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-25 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_csv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='clasificacion',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
