from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('Valid Email Required'))

    def create_user(self, username, email, password=None, display_name=None, **extra_fields):

        if not username:
            raise ValueError(_('Username is required'))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('Email is Required'))

        user = self.model(username=username, email=email, display_name=display_name, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, display_name=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_('Option \"is_staff\" must be true'))

        if not extra_fields.get("is_superuser"):
            raise ValueError(_('Option \"is_superuser\" must be true'))

        if not password:
            raise ValueError(_('Superusers must have a password'))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('Admin Email is Required'))

        user = self.model(username=username, email=email, display_name=display_name, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user.save(using=self._db)
        return user
