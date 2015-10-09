# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_doneinterview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doneinterview',
            name='user_meta',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
