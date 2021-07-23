from accounts.forms import ProfileForm, UserForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import Request

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


def requests(request):
    requests = Request.objects.all()
    return render(
        request, 'crm/requests.html', {'requests': requests})


def request_detail(request, request_id):
    reqq = get_object_or_404(Request, pk=request_id)
    return render(
        request, 'crm/request-deatail.html', {'reqq': reqq})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/dashboard.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requests_count'] = Request.objects.all().count()
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
