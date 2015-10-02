# -*- coding: utf-8 -*-
from django.db import models

class Interview(models.Model):
    title = models.CharField(max_length=250)
    create_date = models.DateTimeField('Дата создания')
    # для указания уровня доступа (0-без авторизации, 1-авториз. 2-подтверждением мыла)
    access = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class TypeInterElem(models.Model):
    # типы элементов опроса.
    type = models.CharField(max_length=25)

    def __unicode__(self):
        return self.type


class InterElem(models.Model):
    interview = models.ForeignKey(Interview)
    # номер позиции в форме.
    num_place = models.SmallIntegerField()
    # type element (text, checkbox, radio
    type_elem = models.OneToOneField(TypeInterElem)
    text_before_elem = models.CharField(max_length=200, blank=True)
    text_after_elem = models.CharField(max_length=200, blank=True)
    default_value = models.CharField(max_length=200, blank=True)
    # варианты значений для radio и select
    radio_select_values = models.CharField(max_length=200, blank=True)
    top_bottom_values = models.CharField(max_length=25, blank=True)

    def __unicode__(self):
        return self.type_elem.type

