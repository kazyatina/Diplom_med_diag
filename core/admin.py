from django.contrib import admin

from .models import ContactInfo, ContactMessage, Doctor, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at")  # добавьте нужные поля
    list_filter = ("created_at",)
    search_fields = ("title",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "is_active")
    list_filter = ("specialty", "is_active")
    search_fields = ("name", "specialty")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("address", "phone", "email")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
