# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-26 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20180126_0954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='body',
            new_name='description',
        ),
    ]
