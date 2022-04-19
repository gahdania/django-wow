# Generated by Django 4.0.2 on 2022-04-17 17:32

import django.core.files.storage
from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_playableclass_icon_spec_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playableclass',
            name='icon',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='icons/class', location=pathlib.PurePosixPath('/home/david/Projects/battlenet/django_wow/src/django_wow/static')), upload_to=''),
        ),
        migrations.AlterField(
            model_name='spec',
            name='icon',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='icons/spec', location=pathlib.PurePosixPath('/home/david/Projects/battlenet/django_wow/src/django_wow/static')), upload_to=''),
        ),
    ]
