# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0003_auto_20151007_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interelem',
            name='text_before_elem',
            field=models.CharField(max_length=200),
        ),
    ]
