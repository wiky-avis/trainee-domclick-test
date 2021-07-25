from django.urls import path

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
    path('requests/', views.RequestsView.as_view(), name='requests'),
    path(
        'requests/<int:pk>/',
        views.RequestDetailView.as_view(),
        name='request-detail'),
    path(
        'requests/<int:pk>/update/',
        views.RequestUpdateView.as_view(),
        name='request_update'),
]
