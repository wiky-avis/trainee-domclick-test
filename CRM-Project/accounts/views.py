from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from accounts.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'])
        login(self.request, user)
        return redirect(reverse('home'))
