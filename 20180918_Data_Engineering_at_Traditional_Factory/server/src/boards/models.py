# boards/models.py
import uuid

from django.conf import settings
from django.db import models
from django.db.models import F, Count, Q

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.


class Device(models.Model):
    mac = models.CharField(max_length=50, unique=True, verbose_name="MAC Address", )
    name = models.CharField(max_length=50, default='-', verbose_name="設備名稱")
    device_type = models.CharField(max_length=50, verbose_name="設備類型")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Install Address")
    online = models.NullBooleanField(default=None, verbose_name="線上狀態")

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    def __str__(self):
        return self.mac


class RecordQueryset(models.QuerySet):
    
    def gte(self, dt):
        datas = self.filter(Q(rs232_time__gte=dt)).order_by('-rs232_time')
        return datas


class RecordManager(models.Manager): 

    def get_queryset(self):
        return RecordQueryset(self.model, using=self._db)

    def gte(self, dt):
        return self.get_queryset().gte(dt)


class Record(models.Model):

    recordid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    machine = models.ForeignKey(
        'Device',
        related_name='devices',
        verbose_name=_('Devices'),
        on_delete=models.CASCADE,
    )
    num = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_('num')
    )
    rs232_time = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('rs232_time')
    )
    create_time = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    objects = RecordManager()
    
    class Meta:
        verbose_name = _('Record')
        verbose_name_plural = _('Records')
        ordering = ('create_time',)

    def __str__(self):
        return str(self.recordid)


class Data(models.Model):

    record = models.OneToOneField(
        'Record',
        related_name='record_datas',
        verbose_name=_('RecordDatas'),
        on_delete=models.CASCADE,
    )
    measure_1 = models.FloatField(null=True, blank=True, verbose_name="量測1")
    measure_2 = models.FloatField(null=True, blank=True, verbose_name="量測2")

    class Meta:
        verbose_name = _('Data')
        verbose_name_plural = _('Datas')

    def __str__(self):
        return str(self.id)