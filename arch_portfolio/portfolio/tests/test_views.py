import datetime as dt
import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from portfolio.models import Category, Contact, Image, Info, Project, Service

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded_gif = SimpleUploadedFile(
            name='small.gif', content=cls.small_gif, content_type='image/gif'
        )
        cls.category = Category.objects.create(title='Заголовок категории')
        cls.project = Project.objects.create(
            title='Project',
            category=cls.category,
            area='Область',
            date=dt.datetime.now(),
            description='Тестовое описание проекта',
        )
        cls.image = Image.objects.create(
            project=cls.project, image=cls.uploaded_gif
        )
        cls.service = Service.objects.create(
            title='Услуга',
            description='Тестовое описание услуги',
            price='от 100 рублей',
        )
        cls.info = Info.objects.create(
            description='Тестовое описание архитектора', image=cls.uploaded_gif
        )
        cls.contact = Contact.objects.create(
            telephone='89991112233',
            email='email@yandex.ru',
            description='Описание контактов',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = Client()

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('home'): 'portfolio/home.html',
            reverse('about'): 'portfolio/about.html',
            reverse('all_projects'): 'portfolio/all_projects.html',
            reverse(
                'project_info', args=[self.project.id]
            ): 'portfolio/project_info.html',
            reverse('services'): 'portfolio/services.html',
            reverse('create_email'): 'portfolio/contacts.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_and_all_projects_pages_show_correct_context(self):
        """Шаблон home и all_projects сформированы с правильным контекстом."""
        templates_list = ['home', 'all_projects']
        for template in templates_list:
            response = self.client.get(reverse(template))
            first_object = response.context['projects'][0]
            projects_title_0 = first_object.title
            projects_category_0 = first_object.category.title
            projects_area_0 = first_object.area
            projects_description_0 = first_object.description
            self.assertEqual(projects_title_0, 'Project')
            self.assertEqual(projects_category_0, 'Заголовок категории')
            self.assertEqual(projects_area_0, 'Область')
            self.assertEqual(
                projects_description_0, 'Тестовое описание проекта'
            )

    def test_services_page_show_correct_context(self):
        """Шаблон services сформирован с правильным контекстом."""
        response = self.client.get(reverse('services'))
        first_object = response.context['services'][0]
        services_title_0 = first_object.title
        services_description_0 = first_object.description
        services_price_0 = first_object.price
        self.assertEqual(services_title_0, 'Услуга')
        self.assertEqual(services_description_0, 'Тестовое описание услуги')
        self.assertEqual(services_price_0, 'от 100 рублей')

    def test_project_info_show_correct_context(self):
        """Шаблон project_info сформирован с правильным контекстом."""
        response = self.client.get(
            reverse('project_info', args=[self.project.id])
        )
        test_project = response.context.get('project')
        test_image = response.context.get('images')[0]
        self.assertEqual(self.project.id, test_project.id)
        self.assertEqual(self.image.image, test_image.image)

    def test_contacts_page_show_correct_context(self):
        """Шаблон contacts сформирован с правильным контекстом."""
        response = self.client.get(reverse('create_email'))
        form_fields = {
            'name': forms.fields.CharField,
            'phone_number': forms.fields.CharField,
            'contact': forms.fields.CharField,
            'memo': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
