# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0002_auto_20151118_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='isbn_number',
            field=models.CharField(unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
