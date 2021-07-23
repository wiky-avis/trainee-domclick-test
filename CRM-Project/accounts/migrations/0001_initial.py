# Generated by Django 3.2.5 on 2021-07-23 12:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('role', models.CharField(choices=[('repair', 'Специалист по ремонту'), ('service', 'Специалист по обслуживанию'), ('consultant', 'Консультант')], default='user', max_length=20, verbose_name='Роль')),
                ('photo', models.ImageField(default='users/avatar5.png', upload_to='users/', verbose_name='Фото')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
