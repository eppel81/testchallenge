# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InterElem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_place', models.SmallIntegerField()),
                ('text_before_elem', models.CharField(max_length=200, blank=True)),
                ('text_after_elem', models.CharField(max_length=200, blank=True)),
                ('default_value', models.CharField(max_length=200, blank=True)),
                ('radio_select_values', models.CharField(max_length=200, blank=True)),
                ('top_bottom_values', models.CharField(max_length=25, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd1\x81\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('access', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TypeInterElem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='interelem',
            name='interview',
            field=models.ForeignKey(to='interview.Interview'),
        ),
        migrations.AddField(
            model_name='interelem',
            name='type_elem',
            field=models.OneToOneField(to='interview.TypeInterElem'),
        ),
    ]
