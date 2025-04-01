from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    last_four_digits = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return  f"{self.name} (****{self.last_four_digits})"