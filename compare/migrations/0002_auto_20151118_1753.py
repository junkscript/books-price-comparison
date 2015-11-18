# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.ManyToManyField(related_name='products', null=True, to='compare.Website', blank=True),
            preserve_default=True,
        ),
    ]
