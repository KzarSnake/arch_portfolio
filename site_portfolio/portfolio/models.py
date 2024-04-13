

from django.db import models


def get_upload_path(instance, filename):
    project = instance.project
    return f'projects/{project}/{filename}'


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        related_name='projects',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    area = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(
        Project,
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to=get_upload_path)
    is_presentation = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Info(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/about/')


class Contact(models.Model):
    telephone = models.IntegerField()
    email = models.EmailField()
    description = models.TextField()


class Mail(models.Model):
    name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=17, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    memo = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return self.name
