import jwt
import uuid

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
)
from django.db import models

#Custom Model UserManager
class UserManager(BaseUserManager):
    def user_create(self, first_name, last_name, email, password, is_customer=True, is_seller=False, is_verified=False, is_active=True, is_admin=False, is_staff=False, otp="default"):
    # create user here
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not email:
            raise ValueError('Users must have an email address')
       
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email.lower()),
            is_customer=is_customer,
            is_seller=is_seller,
            is_verified=is_verified,
            is_active=is_active,
            is_admin=is_admin,
            is_staff=is_staff,
            otp=otp
        )
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password):
    #create super user here
        user = self.user_create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_customer=False,
            is_verfied=False,
            is_seller=False,
            is_active=True,
            is_admin=True,
            is_staff=True,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

#Custom Model User
class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4, auto_created=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True,
    )
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, default="default")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'