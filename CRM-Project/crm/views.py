from accounts.forms import ProfileForm, UserForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic import ListView
from django.db.models import Q
from django.views.generic import ListView
import django_filters
from django_filters import widgets
from django.db import models
from django import forms


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


from distutils.util import strtobool

OPEN = 'open'
WORK = 'work'
CLOSE = 'close'

STATUS = [
    (OPEN, 'Открыта'),
    (WORK, 'В работе'),
    (CLOSE, 'Закрыта')
]


class FilterRequestsView(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=STATUS,
        label=('Статус заявки:')
        )
    specific_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='date',
        widget=forms.SelectDateWidget(),
        label=('Конкретная дата:')
        )
    start_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr=('date__gt'),
        widget=forms.SelectDateWidget(),
        label=('Дата больше чем:')
        )
    end_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr=('date__lt'),
        widget=forms.SelectDateWidget(),
        label=('Дата меньше чем:')
        )

    class Meta:
        model = Request
        fields = ['subject']


class DashboardView(ListView):
    model = Request
    queryset = Request.objects.all()
    template_name = 'crm/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = FilterRequestsView(
            self.request.GET, queryset=Request.objects.all())
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
