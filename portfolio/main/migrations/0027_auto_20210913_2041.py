# Generated by Django 2.2.24 on 2021-09-14 00:41

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20210827_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='award_type',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='main.AwardType'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='project_type',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='main.ProjectType'),
        ),
    ]
