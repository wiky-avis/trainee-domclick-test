from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from accounts.forms import ProfileForm, UserForm

User = get_user_model()


def index(request):
    return render(
        request, 'crm/index.html', {})


def home(request):
    return render(
        request, 'crm/home.html', {})


def clients(request):
    return render(
        request, 'crm/index.html', {})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/dashboard.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.id)
        context['book_list'] = self.request.user
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/profile.html'


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'crm/profile-update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(
            post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Ваш профиль успешно обновлен!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
