# Generated by Django 2.2.24 on 2021-11-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20211101_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='gallery_caption_one',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='gallery_caption_three',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='gallery_caption_two',
            field=models.TextField(blank=True, null=True),
        ),
    ]
