# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-02 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20180201_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='poster',
            field=models.ForeignKey(blank=True, help_text='Dimension 1140px by 555px. Format: PNG or JPG.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
