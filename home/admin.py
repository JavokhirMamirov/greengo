from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', "is_active"]


@admin.register(OwnerOperator)
class OwnerOperatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', "is_active"]


@admin.register(Dispatcher)
class DispatcherAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', "is_active"]


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "track_number",
        "email",
        "is_active",
    ]


@admin.register(InvoiceStatus)
class InvoiceStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'color', "is_active"]

@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'type']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "dispatcher",
        "board",
        "owner",
        "driver",
        "dh",
        "origin",
        "milage",
        "destination",
        "trip_rate",
        "notes",
        "date",
        "status",
    ]
