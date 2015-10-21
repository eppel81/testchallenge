# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder' : 'Электронный адрес'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            tmp = User.objects.get(email=email)
        except User.DoesNotExist:
            if email:
                return email
            else:
                raise forms.ValidationError('Заполните адрес электронной почты')
        raise forms.ValidationError('Такой алрес электронной почты уже зарезервирован')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user