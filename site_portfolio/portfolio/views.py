from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MailForm
from .models import Image, Project, Service, Contact, Info


def home(request):
    """Обработка главной страницы."""
    projects = Project.objects.all()
    return render(
        request,
        'portfolio/home.html',
        {'projects': projects},
    )


def all_projects(request):
    """Обработка страницы со всеми проектами."""
    projects = Project.objects.all()
    return render(
        request, 'portfolio/all_projects.html', {'projects': projects}
    )


def create_email(request):
    """Обработка страницы контактов и формы на ней."""
    contacts = Contact.objects.all()
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            contact = form.cleaned_data['contact']
            memo = form.cleaned_data['memo']

            send_mail(
                f'Новый заказ от {name}',
                f'Контакты для связи: {contact} {phone_number} {memo}',
                'from@example.com',
                ['to@example.com'],
            )
        return redirect('home')
    else:
        form = MailForm()
    return render(request,
                  'portfolio/contacts.html',
                  {'form': form, 'contacts': contacts})


def project_info(request, id):
    """Обработка страницы проекта."""
    project = get_object_or_404(Project, pk=id)
    images = Image.objects.filter(project=id)
    return render(
        request,
        'portfolio/project_info.html',
        {'project': project, 'images': images},
    )


def about(request):
    """Обработка страницы с информацией об авторе."""
    info = Info.objects.all()
    return render(request, 'portfolio/about.html', {'info': info})


def services(request):
    """Обработка страницы с описанием услуг."""
    services = Service.objects.all()
    return render(request, 'portfolio/services.html', {'services': services})
