import datetime as dt

from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from portfolio.models import Category, Project, Service


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(title='Заголовок категории')
        cls.project = Project.objects.create(
            title='Project',
            category=cls.category,
            area='Область',
            date=dt.datetime.now(),
            description='Тестовое описание проекта',
        )
        cls.service = Service.objects.create(
            title='Услуга',
            description='Тестовое описание услуги',
            price='от 100 рублей',
        )

    def setUp(self):
        self.client = Client()

    def test_urls_accessible(self):
        """Набор страниц доступен пользователю."""
        testing_urls = (
            reverse('home'),
            reverse('about'),
            reverse('all_projects'),
            reverse('project_info', args=[self.project.id]),
            reverse('services'),
            reverse('create_email'),
        )
        for url in testing_urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'portfolio/home.html': '/',
            'portfolio/about.html': '/about/',
            'portfolio/all_projects.html': '/projects/',
            'portfolio/project_info.html': '/projects/1/',
            'portfolio/services.html': '/services/',
            'portfolio/contacts.html': '/contacts/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertTemplateUsed(response, template)
