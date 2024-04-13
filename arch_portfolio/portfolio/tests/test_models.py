import datetime as dt
import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from portfolio.models import Category, Image, Project

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageModelTest(TestCase):
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_upload_path(self):
        """Путь загрузки изображения совпадает с ожидаемым."""
        test_image = self.image
        test_path = test_image.image.url
        self.assertEqual(test_path, f'/media/{test_image.image.name}')
