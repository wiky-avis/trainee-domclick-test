from django import forms

from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'status'
        ]


class ClientSendRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'subject',
            'first_name',
            'last_name',
            'email',
            'phone',
            'telegram',
            'notifications',
            'description',
            'data_processing'
            ]


class CreateNewRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'subject',
            'first_name',
            'last_name',
            'email',
            'phone',
            'telegram',
            'description',
            ]
