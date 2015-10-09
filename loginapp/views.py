from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
import pdb

def login(request):
    args = {}
    args['title'] = "Let\'s login"
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        userpass = request.POST.get('userpass', '')
        user = auth.authenticate(username=username, password=userpass)
        if user:
            auth.login(request, user)
            return redirect('/interview/')
        else:
            args['login_error'] = 'User is not found'
            return render(request, 'loginapp/login.html', args)

    return render(request, 'loginapp/login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/interview/')

def register(request):
    c_dict = {}
    if request.method == 'POST':
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            newuser = regform.save()
            return redirect('/auth/login')
    else:
        regform = UserCreationForm()
    c_dict['form'] = regform
    return render(request, 'loginapp/register.html', c_dict)
