from django.db import models

from config import settings


class Request(models.Model):
    subject = models.CharField(
        'Тип заявки',
        max_length=20,
        choices=settings.TYPE,
        default=settings.CONSULTATION
        )
    status = models.CharField(
        'Статус заявки',
        max_length=20,
        choices=settings.STATUS,
        default=settings.OPEN
        )
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    email = models.EmailField('Электронная почта')
    phone = models.CharField('Телефон', max_length=20)
    telegram = models.CharField(
        'Телеграмм ID',
        max_length=20,
        null=True,
        blank=True,
        help_text='Введите свой ID. Если вы не знаете свой ID, вам понадобится'
        ' связаться с ботом @my_id_bot. Напишите ему "/start" и в ответном '
        'сообщении вы должны получить свой уникальный номер идентификации.'
        )
    notifications = models.BooleanField(
        'Хочу получать уведомления на telegram', default=False
        )
    description = models.TextField('Текст заявки')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    data_processing = models.BooleanField(
        'Согласие на обработку персональных данных', default=False
        )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.subject
