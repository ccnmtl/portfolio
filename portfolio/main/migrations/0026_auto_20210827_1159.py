# Generated by Django 2.2.24 on 2021-08-27 15:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('main', '0025_staticpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='discipline',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='entry',
            name='gallery_image_one',
            field=models.ForeignKey(blank=True, help_text='Dimension 300px by 300px. Format: PNG or JPG.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='entry',
            name='gallery_image_three',
            field=models.ForeignKey(blank=True, help_text='Dimension 300px by 300px. Format: PNG or JPG.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='entry',
            name='gallery_image_two',
            field=models.ForeignKey(blank=True, help_text='Dimension 300px by 300px. Format: PNG or JPG.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='entry',
            name='revision_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='Format YYYY-MM-DD. This applies only to a project revision, a MOOC relaunch, or an institute rerun.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='video_title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='entry',
            name='video_url',
            field=models.URLField(blank=True, help_text='URL of the promotional video.'),
        ),
        migrations.AddField(
            model_name='partner',
            name='full_title',
            field=models.TextField(blank=True, help_text='e.g. Dewitt Clinton Professor Emeritus of History'),
        ),
        migrations.AddField(
            model_name='partner',
            name='headshot',
            field=models.ForeignKey(blank=True, help_text='Dimension 300px by 300px. Format: PNG or JPG.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='The main content of this Portfolio entry page.'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='feature_blurb',
            field=models.CharField(blank=True, help_text='A very short blurb on this entry for the feature carousel.', max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='infosheet',
            field=models.ForeignKey(blank=True, help_text='PDF information sheet for printing.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='overview',
            field=models.CharField(blank=True, help_text="A blurb highlighting the project's purpose and effort. Think of it as an elevator pitch.", max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='project_url',
            field=models.URLField(blank=True, help_text="URL of this project's home page."),
        ),
        migrations.AlterField(
            model_name='partner',
            name='short_title',
            field=models.CharField(help_text='e.g. Professor, Librarian, Lecturer', max_length=255),
        ),
        migrations.AddField(
            model_name='entry',
            name='award_type',
            field=modelcluster.fields.ParentalManyToManyField(to='main.AwardType'),
        ),
        migrations.AddField(
            model_name='entry',
            name='project_type',
            field=modelcluster.fields.ParentalManyToManyField(to='main.ProjectType'),
        ),
    ]
