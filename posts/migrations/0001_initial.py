# Generated by Django 2.2.2 on 2019-07-01 01:00

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(default=None, unique=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='posts.Category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(default=None, unique=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='posts.Tag')),
            ],
            options={
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('author_twitter_account', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('sub_title', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('cover', models.ImageField(null=True, upload_to='images/')),
                ('seo_title', models.CharField(default=None, max_length=255)),
                ('seo_description', models.CharField(default=None, max_length=255)),
                ('cover_credits', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True)),
                ('allow_comments', models.BooleanField(default=True, verbose_name='allow_comments')),
                ('published', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='', max_length=10)),
                ('slug', models.SlugField(blank=True, default='', unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='posts.Category')),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='posts.Tag')),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'ordering': ('-created_at',),
            },
        ),
    ]
