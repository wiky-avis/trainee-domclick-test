from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'status'
        ]
