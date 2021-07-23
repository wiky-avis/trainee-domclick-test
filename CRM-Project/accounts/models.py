from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    USER = 'user'
    REPAIR_SPECIALIST = 'repair'
    SERVICE_SPECIALIST = 'service'
    CONSULTANT_SPECIALIST = 'consultant'
    ADMIN = 'administrator'

    ROLES = [
        (REPAIR_SPECIALIST, 'Специалист по ремонту'),
        (SERVICE_SPECIALIST, 'Специалист по обслуживанию'),
        (CONSULTANT_SPECIALIST, 'Консультант'),
        (USER, 'Пользователь без доступа в CRM'),
        (ADMIN, 'Администратор')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Телефон', max_length=20)
    role = models.CharField(
        'Роль', max_length=20, choices=ROLES, default=USER)
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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
