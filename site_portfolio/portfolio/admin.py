from django.contrib import admin

from .models import Category, Contact, Image, Info, Mail, Project, Service


class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Service)
admin.site.register(Contact)
admin.site.register(Info)
admin.site.register(Image, ImageAdmin)
admin.site.register(Mail)
