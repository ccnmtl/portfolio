# Generated by Django 2.2.27 on 2022-03-31 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20220331_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='partners',
        ),
    ]
