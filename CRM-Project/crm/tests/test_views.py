from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from crm.models import Request
from accounts.models import ClientProfile
from config import settings
from django.urls import reverse
from http import HTTPStatus

User = get_user_model()


class CrmPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_repair = User.objects.create_user(
            first_name='Виктория', last_name='Аксентий', username='vika')
        cls.user_repair.profile.role = settings.REPAIR_SPECIALIST

        cls.new_client = ClientProfile.objects.create(
            first_name='Виктория', last_name='Аксентий'
            )

        cls.user_role_isuser = User.objects.create_user(
            first_name='Петя', last_name='Иванов', username='petya')

        cls.request = Request.objects.create(
            subject=settings.REPAIR,
            first_name='Алла',
            last_name='Иванова',
            telegram='1122638601',
            notifications=True,
            description='Текст заявки')

        cls.url_names = [
            reverse('dashboard'),
            reverse('profile_update'),
            reverse('profile'),
            reverse('clients'),
            reverse('new_client'),
            reverse(
                'client_profile', kwargs={'pk': CrmPagesTests.new_client.pk}
                ),
            reverse(
                'client_profile_update',
                kwargs={'pk': CrmPagesTests.new_client.pk}
                ),
            reverse('colleagues'),
            reverse('requests'),
            reverse('new_request'),
            reverse(
                'request_detail', kwargs={'pk': CrmPagesTests.request.pk}
                ),
            reverse(
                'request_update', kwargs={'pk': CrmPagesTests.request.pk}
                ),
            ]

    def setUp(self):
        self.user_auth = Client()
        self.user_auth.force_login(CrmPagesTests.user_repair)
        self.user_role_isuser = Client()
        self.user_role_isuser.force_login(CrmPagesTests.user_role_isuser)

    def test_pages_uses_correct_template(self):
        templates_url_names = {
            'index.html': reverse('index'),
            'home.html': reverse('home'),
            'crm/dashboard.html': reverse('dashboard'),
            'crm/profile_update.html': reverse('profile_update'),
            'crm/profile.html': reverse('profile'),
            'crm/clients_list.html': reverse('clients'),
            'crm/new_client.html': reverse('new_client'),
            'crm/client_profile.html': reverse(
                'client_profile', kwargs={'pk': CrmPagesTests.new_client.pk}
                ),
            'crm/client_profile_update.html': reverse(
                'client_profile_update',
                kwargs={'pk': CrmPagesTests.new_client.pk}
                ),
            'crm/colleagues_list.html': reverse('colleagues'),
            'clients/create_request.html': reverse('client_send_request'),
            'crm/requests.html': reverse('requests'),
            'crm/new_request.html': reverse('new_request'),
            'crm/request_detail.html': reverse(
                'request_detail', kwargs={'pk': CrmPagesTests.request.pk}
                ),
            'crm/request_update.html': reverse(
                'request_update', kwargs={'pk': CrmPagesTests.request.pk}
                ),
            }

        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.user_auth.get(url)
                self.assertTemplateUsed(response, template)

    def test_not_auth_user_not_access_pages(self):
        for url in CrmPagesTests.url_names:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_auth_user_role_isuser_not_access_pages(self):
        for url in CrmPagesTests.url_names:
            with self.subTest(url=url):
                response = self.user_role_isuser.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_new_request_appears_on_pages(self):
        url_pages = (
            reverse('dashboard'),
            reverse('requests')
            )

        for url in url_pages:
            with self.subTest(value=url):
                response = self.user_auth.get(url)
                self.assertContains(
                    response,
                    f'{CrmPagesTests.request.first_name} '
                    f'{CrmPagesTests.request.last_name}'
                    )

    def test_update_status_request(self):
        form_data = {'status': settings.WORK}
        self.user_auth.post(
            reverse(
                'request_update',
                kwargs={'pk': CrmPagesTests.request.pk}),
            data=form_data,
            follow=True
            )

        response = self.user_auth.get(
            reverse(
                'request_detail',
                kwargs={'pk': CrmPagesTests.request.pk})
            )

        request_object = response.context['request']
        self.assertEqual(
            request_object.status, settings.WORK
            )

    def test_delete_request(self):
        self.user_auth.post(
            reverse(
                'request_delete',
                kwargs={'pk': CrmPagesTests.request.pk}))

        response = self.user_auth.get(
            reverse(
                'request_detail',
                kwargs={'pk': CrmPagesTests.request.pk})
            )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertFalse(
            Request.objects.filter(
                id=CrmPagesTests.request.id).exists()
            )

    def test_page_dashboard_filtering_requests_type_and_status(self):
        request_repair = Request.objects.create(
            subject=settings.REPAIR,
            first_name='Ирина',
            last_name='Иванова',
            status=settings.OPEN
            )
        request_service = Request.objects.create(
            subject=settings.SERVICE,
            first_name='Виктория',
            last_name='Бухун',
            status=settings.CLOSE
            )

        subject = 'repair'
        status = 'open'
        response = self.user_auth.get(
            f'/dashboard/?subject={subject}&status={status}'
            )

        self.assertContains(
            response,
            f'{request_repair.first_name} {request_repair.last_name}'
            )
        self.assertNotContains(
            response,
            f'{request_service.first_name} {request_service.last_name}'
            )

    def test_page_dashboard_filtering_requests_two_statuses(self):
        request_repair = Request.objects.create(
            subject=settings.REPAIR,
            first_name='Ирина',
            last_name='Иванова',
            status=settings.OPEN
            )
        request_consult = Request.objects.create(
            subject=settings.CONSULTATION,
            first_name='Жанна',
            last_name='Грачева',
            status=settings.WORK
            )
        request_service = Request.objects.create(
            subject=settings.SERVICE,
            first_name='Виктория',
            last_name='Бухун',
            status=settings.CLOSE
            )

        status = 'open'
        status_2 = 'work'
        response = self.user_auth.get(
            f'/dashboard/?status={status}&status={status_2}'
            )

        self.assertContains(
            response,
            f'{request_repair.first_name} {request_repair.last_name}' and
            f'{request_consult.first_name} {request_consult.last_name}'
            )
        self.assertNotContains(
            response,
            f'{request_service.first_name} {request_service.last_name}'
            )

    def test_page_requests_only_accordance_with_employee_position(self):
        request_repair = Request.objects.create(
            subject=settings.REPAIR,
            first_name='Ирина',
            last_name='Иванова',
            status=settings.OPEN
            )
        request_repair_2 = Request.objects.create(
            subject=settings.REPAIR,
            first_name='Жанна',
            last_name='Грачева',
            status=settings.WORK
            )
        request_service = Request.objects.create(
            subject=settings.SERVICE,
            first_name='Виктория',
            last_name='Бухун',
            status=settings.CLOSE
            )

        response = self.user_auth.get(reverse('requests'))

        self.assertContains(
            response,
            f'{request_repair.first_name} {request_repair.last_name}' and
            f'{request_repair_2.first_name} {request_repair_2.last_name}'
            )
        self.assertNotContains(
            response,
            f'{request_service.first_name} {request_service.last_name}'
            )

    def test_page_clients_new_client_appears_on_pages(self):
        response = self.user_auth.get(reverse('clients'))

        self.assertContains(
            response,
            f'{CrmPagesTests.new_client.first_name} '
            f'{CrmPagesTests.new_client.last_name}'
            )
        self.assertTrue(
            ClientProfile.objects.filter(
                id=CrmPagesTests.new_client.id).exists()
            )

    def test_update_client_profile(self):
        form_data = {
            'email': 'test@test.ru',
            'phone': '89998880088'
            }
        self.user_auth.post(
            reverse(
                'client_profile_update',
                kwargs={'pk': CrmPagesTests.new_client.pk}),
            data=form_data,
            follow=True
            )

        response = self.user_auth.get(
            reverse(
                'client_profile',
                kwargs={'pk': CrmPagesTests.new_client.pk})
            )
        request_object = response.context['user']

        self.assertEqual(
            request_object.first_name, CrmPagesTests.new_client.first_name
            )
        self.assertEqual(
            request_object.last_name, CrmPagesTests.new_client.last_name
            )
        self.assertEqual(request_object.email, CrmPagesTests.new_client.email)
        self.assertEqual(request_object.phone, CrmPagesTests.new_client.phone)

    def test_delete_client_profile(self):
        self.user_auth.post(
            reverse(
                'client_profile_delete',
                kwargs={'pk': CrmPagesTests.new_client.pk}))

        response = self.user_auth.get(
            reverse(
                'client_profile',
                kwargs={'pk': CrmPagesTests.new_client.pk})
            )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertFalse(
            ClientProfile.objects.filter(
                id=CrmPagesTests.new_client.id).exists()
            )
