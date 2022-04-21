from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Region(models.Model):

    tag = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag


class Locale(models.Model):
    language = models.CharField(max_length=2)
    country = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.language.lower()}_{self.country.upper()}"


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(verbose_name=_('Username'), max_length=150, unique=True)
    email = models.EmailField(verbose_name=_('Email Address'), unique=True)
    display_name = models.CharField(verbose_name=_('Display Name'), max_length=150, blank=True, null=True, default='')
    battle_tag = models.CharField(verbose_name=_('BattleTag'), max_length=15, unique=True)
    bnet_id = models.PositiveBigIntegerField(verbose_name=_('Battlenet Account ID'), null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name=_('Account Created'), auto_now=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    preferred_locale = models.ForeignKey(Locale, verbose_name='Locale', on_delete=models.DO_NOTHING,
                                         default=1)
    token = models.JSONField(verbose_name='Access Token', null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("email",)

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')

    def __str__(self):
        return self.display_name if self.display_name else self.username


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    account_number = models.PositiveBigIntegerField(blank=True)

    def __str__(self):
        return f"{self.account_number} - {self.name}"
