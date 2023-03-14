from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ticker = models.CharField(max_length=25)
    value = models.DecimalField(max_digits=15, decimal_places=5)
    amount = models.DecimalField(max_digits=25, decimal_places=5)
    timestamp = models.DateTimeField()