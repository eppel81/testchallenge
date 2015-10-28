# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib
import random
import forms
import models
import pdb


def login(request):
    c_dict = {}
    c_dict['title'] = ""
    c_dict.update(csrf(request))
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['username']
            userpass = cd['userpass']
            user = auth.authenticate(username=username, password=userpass)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('/interview/')
                else:
                    c_dict['login_error'] = 'Подтвердите пожалуйста регистрацию в Вашей электронной почте'
            else:
                c_dict['login_error'] = 'Такого пользователя нет'
                # return render(request, 'loginapp/login.html', c_dict)
    else:
        login_form = forms.LoginForm()
    c_dict['form'] = login_form
    return render(request, 'loginapp/login.html', c_dict)


#  Вьюха логина когда форма была сгенерирована в html
# def login(request):
#     c_dict = {}
#     c_dict['title'] = "Let\'s login"
#     c_dict.update(csrf(request))
#     if request.POST:
#         username = request.POST.get('username', '')
#         userpass = request.POST.get('userpass', '')
#         user = auth.authenticate(username=username, password=userpass)
#         if user:
#             if user.is_active:
#                 auth.login(request, user)
#                 return redirect('/interview/')
#             else:
#                 c_dict['login_error'] = 'Подтвердите пожалуйста регистрацию в Вашей электронной почте'
#         else:
#             c_dict['login_error'] = 'Такого пользователя нет'
#             # return render(request, 'loginapp/login.html', c_dict)
#     return render(request, 'loginapp/login.html', c_dict)


def logout(request):
    auth.logout(request)
    return redirect('/interview/')


def register(request):
    """
    Регистрация с подтверждением по эл. почте.
    """
    c_dict = {}
    c_dict.update(csrf(request))
    if request.method == 'POST':
        regform = forms.RegistrationForm(request.POST)
        c_dict['form'] = regform
        if regform.is_valid():
            # пишем юзера в БД
            user = regform.save()
            username = regform.cleaned_data['username']
            email = regform.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()

            # сохраняем код активации юзера
            new_profile = models.UserProfile(user=user, activation_key=activation_key)
            new_profile.save()

            # шлем на почту подтверждение о регистрации
            email_subject = 'Подтверждение регистрации'
            email_body = 'Спасибо за регистрацию, {0}. Чтобы активировать учетную запись перейдите ' \
                         'по ссылке http://sheltered-harbor-3118.herokuapp.com/auth/confirm/{1}'.format(username, activation_key)
                         # 'по ссылке http://127.0.0.1:8000/auth/confirm/{1}'.format(username, activation_key)

            send_mail(email_subject, email_body, 'testchallengedjango@gmail.com', [email], fail_silently=False)

            c_dict['success_registration'] = 'Не забудьте подтвердить регистрацию в электронной почте'
            return render(request, 'loginapp/login.html', c_dict)
    else:
        regform = forms.RegistrationForm()
        c_dict['form'] = regform
    return render(request, 'loginapp/register.html', c_dict)



# def register(request):
#     """
#     Регистрация без подтверждения эл. почты.
#     """
#     c_dict = {}
#     if request.method == 'POST':
#         regform = UserCreationForm(request.POST)
#         if regform.is_valid():
#             newuser = regform.save()
#             # return redirect('/auth/login')
#             c_dict['success_registration'] = 'Вы успешно зарегистрированы, теперь можно и авторизироваться'
#             return render(request, 'loginapp/login.html', c_dict)
#     else:
#         regform = UserCreationForm()
#     c_dict['form'] = regform
#     return render(request, 'loginapp/register.html', c_dict)


def register_confirm(request, activation_key):
    """
    Функция подтверждения регистрации. Проверяем activation_key
    """
    c_dict = {}

    try:
        user_profile = models.UserProfile.objects.get(activation_key=activation_key)
    except Exception:
        c_dict['success_registration'] = 'Ваш пользователь отсутствует в БД. Попробуйте выполнить регистрацию заново.'
        return render(request, 'loginapp/login.html', c_dict)

    # вруг юзер уже залогинен тогда перенаправим его на стартовую страницу
    if request.user.is_authenticated():
        return redirect('/interview/')

    user = user_profile.user
    if not user.is_active:
        user.is_active = True
        user.save()
        c_dict['success_registration'] = 'Вы успешно зарегистрированы, теперь можно и авторизироваться.'
    return render(request, 'loginapp/login.html', c_dict)
    # return redirect('/interview/')
