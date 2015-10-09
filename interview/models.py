# -*- coding: utf-8 -*-
from django.db import models
# from django.contrib.auth.models import User

class Interview(models.Model):
    """
    Interview's model/
    """
    description = models.CharField(max_length=250)
    create_date = models.DateTimeField('Дата создания')
    # для указания уровня доступа (0-без авторизации, 1-авториз. 2-подтверждением мыла)
    access = models.IntegerField(default=0)

    def __unicode__(self):
        return self.description


class InterElem(models.Model):
    """
    Model with elements of interviews
    """
    type_elem_list = (
        ('txt', 'Text'),
        ('radio', 'Radio button'),
        ('select', 'Select'),
        ('mselect', 'Multi Select'),
        ('dpicker', 'Digit picker'),
        ('check', 'Checkbox'),
    )

    interview = models.ForeignKey(Interview)
    # type element (text, checkbox, radio
    type_elem = models.CharField(max_length=10, choices=type_elem_list, default='txt')
    text_before_elem = models.CharField(max_length=200)
    text_after_elem = models.CharField(max_length=200, blank=True)
    default_value = models.CharField(max_length=200, blank=True)
    # варианты значений для radio и select
    radio_select_values = models.CharField(max_length=200, blank=True)
    top_bottom_values = models.CharField(max_length=25, blank=True)
    # номер позиции на форме.
    position = models.SmallIntegerField()

    def __unicode__(self):
        return self.text_before_elem

class DoneInterview(models.Model):
    """
    Model with users answers
    """
    interelem = models.ForeignKey(InterElem)
    user_id = models.IntegerField()
    resp = models.CharField(max_length=200, blank=True)
    user_meta = models.CharField(max_length=200, blank=True)
