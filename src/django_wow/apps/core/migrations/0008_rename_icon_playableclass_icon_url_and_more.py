# Generated by Django 4.0.2 on 2022-04-17 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_racename_last_updated_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playableclass',
            old_name='icon',
            new_name='icon_url',
        ),
        migrations.RenameField(
            model_name='spec',
            old_name='icon',
            new_name='icon_url',
        ),
    ]
