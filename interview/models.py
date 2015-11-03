# -*- coding: utf-8 -*-
from django.db import models
# from django.contrib.auth.models import User

class Interview(models.Model):
    """
    Interview's model/
    """
    type_access = (
        ('0', 'Для всех'),
        ('1', 'Для зарегистрированных'),
    )

    description = models.CharField(max_length=250, verbose_name='Название')
    wide_description = models.TextField(blank=True, verbose_name='Описание')
    create_date = models.DateTimeField('Дата создания')
    # для указания уровня доступа (0-без авторизации, 1-авториз. 2-подтверждением мыла)
    # access = models.IntegerField(default=0)
    access = models.CharField(max_length=2, choices=type_access, default='0', verbose_name='Уровень доступа')

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
    type_elem = models.CharField(max_length=10, choices=type_elem_list, default='txt', verbose_name='Тип ответа на вопрос')
    text_before_elem = models.CharField(max_length=200, verbose_name='Текст вопроса')
    text_after_elem = models.CharField(max_length=200, blank=True, verbose_name='Вспомогательный текст')
    default_value = models.CharField(max_length=200, blank=True, verbose_name='Значение по умолчанию')
    # варианты значений для radio и select
    radio_select_values = models.CharField(max_length=200, blank=True, verbose_name='Значения для radio и select')
    top_bottom_values = models.CharField(max_length=25, blank=True, verbose_name='Min и Max для Digit picker')
    # номер позиции на форме.
    position = models.SmallIntegerField(verbose_name='Позиция вопроса в списке')

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
