# Generated by Django 4.0.2 on 2022-04-17 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_playableclass_icon_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spec',
            name='icon_url',
        ),
    ]
