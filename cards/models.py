from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    censoredNumber = models.CharField(max_length=16)
    isValid = models.BooleanField(default=False)