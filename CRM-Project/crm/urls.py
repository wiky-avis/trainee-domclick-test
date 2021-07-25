from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('crm/', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path(
        'profile-update/',
        views.ProfileUpdateView.as_view(),
        name='profile-update'
        ),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('clients/', views.ClientsView.as_view(), name='clients'),
    path(
        'clients/new/', views.CreateNewClientView.as_view(), name='new_client'
        ),
    path(
        'client-profile/<int:pk>/',
        views.ClientProfileView.as_view(),
        name='client_profile'
        ),
    path(
        'client-profile/<int:pk>/update/',
        views.ClientProfileUpdateView.as_view(),
        name='client_profile_update'
        ),
    path(
        'client-profile/<int:pk>/delete/',
        views.DeleteClientView.as_view(),
        name='client_profile_delete'
        ),
    path('colleagues/', views.ColleaguesView.as_view(), name='colleagues'),
    path(
        'send-request/',
        views.ClientSendRequestView.as_view(),
        name='client_send_request'
        ),
    path('requests/', views.RequestsView.as_view(), name='requests'),
    path('requests/new/', views.CreateRequestView.as_view(), name='new_request'),
    path(
        'requests/<int:pk>/',
        views.RequestDetailView.as_view(),
        name='request-detail'),
    path(
        'requests/<int:pk>/update/',
        views.RequestUpdateView.as_view(),
        name='request_update'),
    path(
        'requests/<int:pk>/delete/',
        views.RequestDeleteView.as_view(),
        name='request_delete'),
    path(
        'send-request-succes/',
        TemplateView.as_view(template_name='crm/create_request_done.html'),
        name='send-request-succes'
    ),
]
