from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    # USERNAME_FIELD =  'email'


class Profile(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=80)
    suite = models.CharField(max_length=50)
    apartment = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField('first_name', max_length=70, blank=True)
    last_name = models.CharField('last_name', max_length=70, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'

    def save(self, *args, **kwargs):
        self.email = self.user.email
        self.phone_number = self.user.phone_number
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name

        super().save(*args, **kwargs)






