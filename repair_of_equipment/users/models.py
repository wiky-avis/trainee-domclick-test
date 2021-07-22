from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    REPAIR_SPECIALIST = 'repair'
    SERVICE_SPECIALIST = 'service'
    CONSULTANT_SPECIALIST = 'consultant'

    ROLES = [
        (REPAIR_SPECIALIST, 'Специалист по ремонту'),
        (SERVICE_SPECIALIST, 'Специалист по обслуживанию'),
        (CONSULTANT_SPECIALIST, 'Консультант')
    ]

    email = models.EmailField(
        'Электронная почта', unique=True, db_index=True)
    phone = models.CharField(
        'Телефон', max_length=20, unique=True, db_index=True)
    role = models.CharField(
        'Права', max_length=20, choices=ROLES, default=USER)
    photo = models.ImageField(
        'Фото',
        upload_to='users/',
        default='users/avatar5.png'
        )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_repair_specialist(self):
        return self.role == self.REPAIR_SPECIALIST

    @property
    def is_service_specialist(self):
        return self.role == self.SERVICE_SPECIALIST

    @property
    def is_consultant_specialist(self):
        return self.role == self.CONSULTANT_SPECIALIST
