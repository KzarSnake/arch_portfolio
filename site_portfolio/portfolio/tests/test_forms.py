from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse


class MailTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_form_send_mail(self):
        """Валидная форма отправляет письмо администратору сайта."""
        form_data = {
            'name': 'Имя Фамилия',
            'phone_number': '98887774411',
            'contact': '/gsnake',
            'memo': 'Тестовое письмо',
        }
        response = self.client.post(
            reverse('create_email'), data=form_data, follow=True
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Новый заказ от Имя Фамилия')
        self.assertEqual(
            mail.outbox[0].body,
            'Контакты для связи: /gsnake 98887774411 Тестовое письмо')
        self.assertRedirects(response, reverse('home'))
