# flake8: noqa
# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-11 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20180109_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='overview',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='entry',
            name='release_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, help_text='The main content of this Portfolio entry page'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='infosheet',
            field=models.ForeignKey(blank=True, help_text='help me', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='project_url',
            field=models.URLField(blank=True, help_text='URL of this project'),
        ),
    ]
