from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from config import settings

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Телефон', max_length=20)
    role = models.CharField(
        'Роль', max_length=20, choices=settings.ROLES, default=settings.USER)
    photo = models.ImageField(
        'Фото',
        upload_to='users/',
        default='users/avatar5.png'
        )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили позьзователей'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def is_user(self):
        return self.role == settings.USER

    @property
    def is_repair_specialist(self):
        return self.role == settings.REPAIR_SPECIALIST

    @property
    def is_service_specialist(self):
        return self.role == settings.SERVICE_SPECIALIST

    @property
    def is_consultant_specialist(self):
        return self.role == settings.CONSULTANT_SPECIALIST


class ClientProfile(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    email = models.EmailField('Почта')
    phone = models.CharField('Телефон', max_length=20)
    telegram = models.CharField(
        'Телеграмм ID', max_length=20, null=True, blank=True
        )

    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиентов'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
