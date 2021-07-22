from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Request

User = get_user_model()


def index(request):
    return render(
        request, 'index.html', {})


def profile_employee(request, username):
    employee = get_object_or_404(User, username=username)
    requests = Request.objects.all()
    return render(
        request, 'profile_employee.html', {'employee': employee, 'requests_count': requests.count(), 'requests': requests})
