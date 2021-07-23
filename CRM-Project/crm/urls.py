from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crm/', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile-update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('clients/', views.clients, name='clients'),
    path('requests/', views.requests, name='requests'),
    path('requests/<int:request_id>/', views.request_detail, name='request-detail'),
]
