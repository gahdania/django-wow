# Generated by Django 4.0.2 on 2022-04-17 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_icon_url_playableclass_icon_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='racename',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='connectedrealm',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='faction',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='realmtype',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='stat',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='realm',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
