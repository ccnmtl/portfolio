# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-26 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20180126_1106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='entry',
            name='partners',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='main.Partner'),
        ),
        migrations.AddField(
            model_name='partner',
            name='sort_order',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
