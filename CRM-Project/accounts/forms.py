from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ClientProfile, Profile


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30, required=False, help_text='Ввведите свое имя')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Введите свою фамилию')
    email = forms.EmailField(max_length=254, help_text='Введите свой email')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone',
            'photo'
        ]


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'telegram'
        ]
