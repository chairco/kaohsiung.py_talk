# boards/models.py
from django.contrib import admin

from boards.models import Device, Data, Record


class DataInline(admin.TabularInline):
    model = Data
    extra = 1


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'mac', 'name', 'device_type', 'address',
        'online'
    ]


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = [
        'recordid', 'machine', 'num',
        'rs232_time', 'create_time'
    ]
    inlines = (
        DataInline,
    )