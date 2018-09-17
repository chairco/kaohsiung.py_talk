# Generated by Django 2.1.1 on 2018-09-17 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='num',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='num'),
        ),
        migrations.AlterField(
            model_name='data',
            name='record',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='record_datas', to='boards.Record', verbose_name='RecordDatas'),
        ),
    ]
