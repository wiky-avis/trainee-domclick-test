from django.contrib import admin

from .models import ClientProfile, Profile

admin.site.register(Profile)
admin.site.register(ClientProfile)
