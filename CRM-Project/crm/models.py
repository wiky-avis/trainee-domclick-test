from django.db import models


class Request(models.Model):

    REPAIR = 'repair'
    SERVICE = 'service'
    CONSULTATION = 'consultant'

    OPEN = 'open'
    WORK = 'work'
    CLOSE = 'close'

    TYPE = [
        (REPAIR, 'Заявка на ремонт'),
        (SERVICE, 'Заявка на обслуживание'),
        (CONSULTATION, 'Заявка на консультацию'),
    ]

    STATUS = [
        (OPEN, 'Открыта'),
        (WORK, 'В работе'),
        (CLOSE, 'Закрыта')
    ]

    subject = models.CharField(
        'Тип заявки',
        max_length=20,
        choices=TYPE,
        default=CONSULTATION
        )
    status = models.CharField(
        'Статус заявки', max_length=20, choices=STATUS, default=OPEN
        )
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    email = models.EmailField('Электронная почта')
    phone = models.CharField('Телефон', max_length=20)
    telegram = models.CharField(
        'Телеграм', max_length=20, null=True, blank=True
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
