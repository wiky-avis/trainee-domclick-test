from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    user = request.user
    return render(
        request, 'index.html', {'user': user})


def profile_employee(request, username):
    employee = get_object_or_404(User, username=username)
    return render(
        request, 'profile_employee.html', {'employee': employee})
