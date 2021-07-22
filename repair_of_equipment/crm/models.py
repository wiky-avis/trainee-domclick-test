from django.db import models


class Request(models.Model):

    REPAIR = 'repair'
    SERVICE = 'service'
    CONSULTATION = 'consultation'

    OPEN = 'open'
    WORK = 'work'
    CLOSE = 'close'

    TYPE = [
        (REPAIR, 'Заявка на ремонт'),
        (SERVICE, 'Заявка на обслуживание'),
        (CONSULTATION, 'Заявка на консультацию')
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
        default='Выберите тип заявки'
        )
    status = models.CharField(
        'Статус заявки', max_length=20, choices=STATUS, default=OPEN
        )
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    email = models.EmailField('Электронная почта')
    phone = models.CharField('Телефон', max_length=20)
    telegram = models.CharField('Телеграм', max_length=20)
    description = models.TextField('Текст заявки')
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('subject', 'status')
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.subject

    @property
    def is_repair(self):
        return self.subject == self.REPAIR

    @property
    def is_service(self):
        return self.subject == self.SERVICE

    @property
    def is_consultation(self):
        return self.subject == self.CONSULTATION

    @property
    def is_open(self):
        return self.status == self.OPEN

    @property
    def is_work(self):
        return self.status == self.WORK

    @property
    def is_close(self):
        return self.status == self.CLOSE
