# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('brand_logo', models.ImageField(upload_to=b'commerce/brand')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color_name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('material_name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('sku_code', models.CharField(max_length=255)),
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
            name='ProductPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_img', models.ImageField(upload_to=b'commerce/product')),
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
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=12)),
                ('vendor_code', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VendorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vendor_type', models.CharField(max_length=255)),
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
            model_name='vendor',
            name='vendor_type',
            field=models.ManyToManyField(to='compare.VendorType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.ManyToManyField(related_name='products', to='compare.Website'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(to='compare.Brand'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(to='compare.Color'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='featured_image',
            field=models.ForeignKey(related_name='featured', blank=True, to='compare.ProductPhoto', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.ManyToManyField(to='compare.Material'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='photos',
            field=models.ManyToManyField(to='compare.ProductPhoto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(to='compare.ProductCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='product_subcategory',
            field=models.ForeignKey(to='compare.ProductSubcategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='compare.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ManyToManyField(to='compare.Vendor'),
            preserve_default=True,
        ),
    ]
