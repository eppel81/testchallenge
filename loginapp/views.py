# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
import pdb

def login(request):
    c_dict = {}
    c_dict['title'] = "Let\'s login"
    c_dict.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        userpass = request.POST.get('userpass', '')
        user = auth.authenticate(username=username, password=userpass)
        if user:
            auth.login(request, user)
            return redirect('/interview/')
        else:
            c_dict['login_error'] = 'User is not found'
            return render(request, 'loginapp/login.html', c_dict)
    return render(request, 'loginapp/login.html', c_dict)


def logout(request):
    auth.logout(request)
    return redirect('/interview/')


def register(request):
    c_dict = {}
    if request.method == 'POST':
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            newuser = regform.save()
            # return redirect('/auth/login')
            c_dict['success_registration'] = 'Вы успешно зарегистрированы, теперь можно и авторизироваться'
            return render(request, 'loginapp/login.html', c_dict)
    else:
        regform = UserCreationForm()
    c_dict['form'] = regform
    return render(request, 'loginapp/register.html', c_dict)
