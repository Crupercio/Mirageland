from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    coins = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.username
