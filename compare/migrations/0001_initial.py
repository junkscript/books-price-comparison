# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('featured_image', models.ImageField(null=True, upload_to=b'compare/', blank=True)),
                ('image_url', models.URLField(null=True, blank=True)),
                ('isbn_number', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('visit_count', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_category', models.CharField(max_length=200)),
                ('featured_image', models.ImageField(upload_to=b'commerce/product_category')),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductSubcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_subcategory', models.CharField(max_length=200)),
                ('featured_image', models.ImageField(upload_to=b'commerce/product_subcategory')),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inside_text', models.TextField()),
                ('product', models.ForeignKey(related_name='p_reviews', to='compare.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('product_url', models.URLField()),
                ('price', models.FloatField(default=0.0)),
                ('sentiment_rating', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.ManyToManyField(related_name='products', to='compare.Website'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(blank=True, to='compare.ProductCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='product_subcategory',
            field=models.ForeignKey(blank=True, to='compare.ProductSubcategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='compare.Tag', null=True, blank=True),
            preserve_default=True,
        ),
    ]
