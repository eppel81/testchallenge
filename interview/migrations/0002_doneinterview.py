# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoneInterview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('resp', models.CharField(max_length=200, blank=True)),
                ('user_meta', models.CharField(max_length=250, blank=True)),
                ('interelem', models.ForeignKey(to='interview.InterElem')),
            ],
        ),
    ]
