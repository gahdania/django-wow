# Generated by Django 4.0.2 on 2022-04-09 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_account_user_alter_user_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.JSONField(blank=True, null=True, verbose_name='Access Token'),
        ),
    ]