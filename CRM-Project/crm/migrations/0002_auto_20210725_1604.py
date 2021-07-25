# Generated by Django 3.2.5 on 2021-07-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='data_processing',
            field=models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных'),
        ),
        migrations.AddField(
            model_name='request',
            name='notifications',
            field=models.BooleanField(default=False, verbose_name='Хочу получать уведомления на telegram'),
        ),
        migrations.AlterField(
            model_name='request',
            name='subject',
            field=models.CharField(choices=[('repair', 'Заявка на ремонт'), ('service', 'Заявка на обслуживание'), ('consultant', 'Заявка на консультацию')], default='consultant', max_length=20, verbose_name='Тип заявки'),
        ),
        migrations.AlterField(
            model_name='request',
            name='telegram',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телеграм'),
        ),
    ]
