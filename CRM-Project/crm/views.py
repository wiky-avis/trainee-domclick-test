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


class TypeStatus:

    def get_type_repair(self):
        return Request.objects.filter(subject=Request.REPAIR)

    def get_type_service(self):
        return Request.objects.filter(subject=Request.SERVICE)

    def get_type_consultation(self):
        return Request.objects.filter(subject=Request.CONSULTATION)

    def get_status_open(self):
        return Request.objects.filter(subject=Request.REPAIR)

    def get_status_work(self):
        return Request.objects.filter(subject=Request.SERVICE)

    def get_status_close(self):
        return Request.objects.filter(subject=Request.CONSULTATION)

    def get_all(self):
        return Request.objects.all()


class DashboardView(TypeStatus, ListView):
    model = Request
    queryset = Request.objects.all()
    template_name = 'crm/dashboard.html'


class FilterRequestsView(TypeStatus, ListView):
    template_name = 'crm/dashboard.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = Request.objects.filter(
            Q(subject__in=self.request.GET.getlist('type_repair')) |
            Q(subject__in=self.request.GET.getlist('type_service')) |
            Q(subject__in=self.request.GET.getlist('type_consultation')) |
            Q(status__in=self.request.GET.getlist('status_open')) |
            Q(status__in=self.request.GET.getlist('status_work')) |
            Q(status__in=self.request.GET.getlist('status_close'))
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['type_repair'] = ''.join(
            [f'type_repair={x}&' for x in self.request.GET.getlist(
                'type_repair')]
            )
        context['type_service'] = ''.join(
            [f'type_service={x}&' for x in self.request.GET.getlist(
                'type_service')]
            )
        context['type_consultation'] = ''.join(
            [f'type_consultation={x}&' for x in self.request.GET.getlist(
                'type_consultation')]
            )
        context['status_open'] = ''.join(
            [f'status_open={x}&' for x in self.request.GET.getlist(
                'status_open')]
            )
        context['status_work'] = ''.join(
            [f'status_work={x}&' for x in self.request.GET.getlist(
                'status_work')]
            )
        context['status_close'] = ''.join(
            [f'status_close={x}&' for x in self.request.GET.getlist(
                'status_close')]
            )
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
