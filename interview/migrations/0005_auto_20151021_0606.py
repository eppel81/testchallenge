# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0004_auto_20151009_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interelem',
            name='default_value',
            field=models.CharField(max_length=200, verbose_name=b'\xd0\x97\xd0\xbd\xd0\xb0\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbf\xd0\xbe \xd1\x83\xd0\xbc\xd0\xbe\xd0\xbb\xd1\x87\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8e', blank=True),
        ),
        migrations.AlterField(
            model_name='interelem',
            name='position',
            field=models.SmallIntegerField(verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb7\xd0\xb8\xd1\x86\xd0\xb8\xd1\x8f \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd0\xb0 \xd0\xb2 \xd1\x81\xd0\xbf\xd0\xb8\xd1\x81\xd0\xba\xd0\xb5'),
        ),
        migrations.AlterField(
            model_name='interelem',
            name='radio_select_values',
            field=models.CharField(max_length=200, verbose_name=b'\xd0\x97\xd0\xbd\xd0\xb0\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xb4\xd0\xbb\xd1\x8f radio \xd0\xb8 select', blank=True),
        ),
        migrations.AlterField(
            model_name='interelem',
            name='text_after_elem',
            field=models.CharField(max_length=200, verbose_name=b'\xd0\x92\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbc\xd0\xbe\xd0\xb3\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82', blank=True),
        ),
        migrations.AlterField(
            model_name='interelem',
            name='text_before_elem',
            field=models.CharField(max_length=200, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xba\xd1\x81\xd1\x82 \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='interelem',
            name='top_bottom_values',
            field=models.CharField(max_length=25, verbose_name=b'Min \xd0\xb8 Max \xd0\xb4\xd0\xbb\xd1\x8f Digit picker', blank=True),
        ),
        migrations.AlterField(
            model_name='interelem',
            name='type_elem',
            field=models.CharField(default=b'txt', max_length=10, verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82\xd0\xb0 \xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81', choices=[(b'txt', b'Text'), (b'radio', b'Radio button'), (b'select', b'Select'), (b'mselect', b'Multi Select'), (b'dpicker', b'Digit picker'), (b'check', b'Checkbox')]),
        ),
    ]
