# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-26 15:29
from __future__ import unicode_literals

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20180126_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
