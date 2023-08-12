from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, cellphone_number, password, **extra_fields):
        if not cellphone_number and not email:
            raise ValueError(_('cell number or email is required'))
        user = self.model(cellphone_number=cellphone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, cellphone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email=None, cellphone_number=cellphone_number, password=password, **extra_fields)
