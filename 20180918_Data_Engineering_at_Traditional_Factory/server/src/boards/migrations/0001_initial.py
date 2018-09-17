# Generated by Django 2.1.1 on 2018-09-17 08:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure_1', models.FloatField(blank=True, null=True, verbose_name='量測1')),
                ('measure_2', models.FloatField(blank=True, null=True, verbose_name='量測2')),
            ],
            options={
                'verbose_name': 'Data',
                'verbose_name_plural': 'Datas',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=50, unique=True, verbose_name='MAC Address')),
                ('name', models.CharField(default='-', max_length=50, verbose_name='設備名稱')),
                ('device_type', models.CharField(max_length=50, verbose_name='設備類型')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Install Address')),
                ('online', models.NullBooleanField(default=None, verbose_name='線上狀態')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('recordid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rs232_time', models.DateTimeField(blank=True, null=True, verbose_name='rs232_time')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='boards.Device', verbose_name='Devices')),
            ],
            options={
                'verbose_name': 'Record',
                'verbose_name_plural': 'Records',
                'ordering': ('create_time',),
            },
        ),
        migrations.AddField(
            model_name='data',
            name='record',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='record_data', to='boards.Record', verbose_name='RecordDatas'),
        ),
    ]