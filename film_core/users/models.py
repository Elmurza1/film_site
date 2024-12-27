from django.db import models
from django.contrib.auth.models import  AbstractUser
# Create your models here.
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    """модель для пользователя"""
    from film.models import Movi
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    favorite_movi = models.ManyToManyField(Movi)

    email = models.EmailField(
        unique=True,
        db_index=True
    )
    objects = CustomUserManager()
