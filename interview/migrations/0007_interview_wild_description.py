# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0006_auto_20151022_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='wild_description',
            field=models.TextField(blank=True),
        ),
    ]
