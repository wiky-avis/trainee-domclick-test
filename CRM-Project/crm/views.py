from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, DeleteView

from accounts.forms import ProfileForm, UserForm, ClientProfileForm
from accounts.models import Profile, ClientProfile

from .filters import FilterRequestsDashboardView, FilterRequestsView
from .forms import RequestForm, ClientSendRequestForm, CreateNewRequestForm
from .models import Request
from .telegramm import send_message, bot_client, CHAT_ID, logger


User = get_user_model()


class IndexView(TemplateView):
    template_name = 'crm/index.html'


class HomeView(TemplateView):
    template_name = 'crm/home.html'


class ColleaguesView(LoginRequiredMixin, ListView):
    model = User
    queryset = User.objects.all()
    template_name = 'crm/colleagues_list.html'


class ClientSendRequestView(TemplateView):
    request_form = ClientSendRequestForm
    template_name = 'crm/create_request.html'

    def post(self, request):
        post_data = request.POST or None
        send_request_form = ClientSendRequestForm(post_data)

        if send_request_form.is_valid():
            send_request_form.save()
            try:
                telegramm_id = send_request_form.cleaned_data.get('telegram')
                notifications = send_request_form.cleaned_data.get(
                    'notifications')
                if telegramm_id and notifications is True:
                    send_message(
                        chat_id=telegramm_id,
                        message='Заявка успешно создана!',
                        bot_client=bot_client
                        )
            except Exception as error:
                logger.error(f'Бот столкнулся с ошибкой: {error}')
                send_message(
                    message='Бот столкнулся с ошибкой',
                    chat_id=CHAT_ID,
                    bot_client=bot_client
                    )
            messages.error(request, 'Заявка успешно создана!')
            return redirect('send-request-succes')

        context = self.get_context_data(send_request_form=send_request_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CreateRequestView(LoginRequiredMixin, TemplateView):
    new_request_form = CreateNewRequestForm
    template_name = 'crm/new_request.html'

    def post(self, request):
        post_data = request.POST or None
        new_request_form = CreateNewRequestForm(post_data)

        if new_request_form.is_valid():
            new_request_form.save()
            messages.error(request, 'Заявка успешно создана!')
            return redirect('dashboard')

        context = self.get_context_data(new_request_form=new_request_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = Request

    def post(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        req.delete()
        return redirect('requests')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RequestsView(LoginRequiredMixin, ListView):
    model = Request
    queryset = Request.objects.all()
    template_name = 'crm/requests.html'

    def get_context_data(self, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.request.user.id)
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = FilterRequestsView(
            self.request.GET,
            queryset=Request.objects.filter(subject=profile.role)
            )
        return context


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    queryset = Request.objects.all()
    template_name = 'crm/request_detail.html'
    context_object_name = 'request'


class RequestUpdateView(LoginRequiredMixin, TemplateView):
    request_form = RequestForm
    template_name = 'crm/request_update.html'

    def post(self, request, pk):
        post_data = request.POST or None
        req = get_object_or_404(Request, pk=pk)
        request_form = RequestForm(post_data, instance=req)

        if request_form.is_valid():
            request_form.save()
            try:
                telegramm_id = req.telegram
                notifications = req.notifications
                status = request_form.cleaned_data.get('status')
                if telegramm_id and notifications is True:
                    if status == 'work' or status == 'close':
                        send_message(
                            chat_id=telegramm_id,
                            message=f'Статус заявки изменен на {status}',
                            bot_client=bot_client
                            )
            except Exception as error:
                logger.error(f'Бот столкнулся с ошибкой: {error}')
                send_message(
                    message='Бот столкнулся с ошибкой',
                    chat_id=CHAT_ID,
                    bot_client=bot_client
                    )
            messages.error(request, 'Заявка успешно обновлена!')
            return redirect('request_update', req.pk)

        context = self.get_context_data(request_form=request_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = get_object_or_404(
            Request, pk=self.kwargs.get('pk')
            )
        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = Request
    queryset = Request.objects.all()
    template_name = 'crm/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = FilterRequestsDashboardView(
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


class ClientsView(LoginRequiredMixin, ListView):
    model = ClientProfile
    queryset = ClientProfile.objects.all()
    template_name = 'crm/clients_list.html'


class ClientProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/client_profile.html'

    def get(self, request, pk, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user'] = get_object_or_404(ClientProfile, pk=pk)
        return self.render_to_response(context)


class ClientProfileUpdateView(LoginRequiredMixin, TemplateView):
    profile_form = ClientProfileForm
    template_name = 'crm/client_profile-update.html'

    def post(self, request, pk):
        post_data = request.POST or None
        client = get_object_or_404(ClientProfile, pk=pk)
        profile_form = ClientProfileForm(post_data, instance=client)

        if profile_form.is_valid():
            profile_form.save()
            messages.error(request, 'Профиль клиента успешно обновлен!')
            return redirect('client_profile', client.pk)

        context = self.get_context_data(profile_form=profile_form, client=client)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CreateNewClientView(LoginRequiredMixin, TemplateView):
    profile_form = ClientProfileForm
    template_name = 'crm/new_client.html'

    def post(self, request):
        post_data = request.POST or None
        profile_form = ClientProfileForm(post_data)

        if profile_form.is_valid():
            profile_form.save()
            messages.error(request, 'Клиент успешно создан!')
            return redirect('clients')

        context = self.get_context_data(profile_form=profile_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DeleteClientView(LoginRequiredMixin, DeleteView):
    model = ClientProfile

    def post(self, request, pk):
        req = get_object_or_404(ClientProfile, pk=pk)
        req.delete()
        return redirect('clients')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
