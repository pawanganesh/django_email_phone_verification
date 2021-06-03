import random

from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = (instance.first_name + "." + instance.last_name).lower()
        counter = 1
        while User.objects.filter(username=username):
            username += str(counter)
            counter += 1
        instance.username = username


def generate_code():
    number_list = [x for x in range(10)]
    code_items = []

    for i in range(6):
        num = random.choice(number_list)
        code_items.append(num)
    code_string = "".join(str(item) for item in code_items)
    return code_string


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("User must have first name")
        if not last_name:
            raise ValueError("User must have last name")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(verbose_name='email', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified_email = models.BooleanField(default=False)
    auth_token_email = models.CharField(max_length=6, blank=True)

    phone_number = models.CharField(max_length=14, null=True, blank=True)
    is_verified_phone = models.BooleanField(default=False)
    auth_token_phone = models.CharField(max_length=6, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.user.email:
            self.auth_token_email = generate_code()
        if self.phone_number:
            self.auth_token_phone = generate_code()

        print(self.auth_token_phone)
        print(self.auth_token_email)

        super().save(*args, **kwargs)


models.signals.pre_save.connect(set_username, sender=User)
