# Generated by Django 3.2.5 on 2021-07-25 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('repair', 'Заявка на ремонт'), ('service', 'Заявка на обслуживание'), ('consultant', 'Заявка на консультацию')], default='consultant', max_length=20, verbose_name='Тип заявки')),
                ('status', models.CharField(choices=[('open', 'Открыта'), ('work', 'В работе'), ('close', 'Закрыта')], default='open', max_length=20, verbose_name='Статус заявки')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('telegram', models.CharField(blank=True, max_length=20, null=True, verbose_name='Телеграм')),
                ('notifications', models.BooleanField(default=False, verbose_name='Хочу получать уведомления на telegram')),
                ('description', models.TextField(verbose_name='Текст заявки')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('data_processing', models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ('-created',),
            },
        ),
    ]
