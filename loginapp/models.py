# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Расширяем модель User для хранения ключа активации
    """
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username
