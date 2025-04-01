from django.db import models
from django.contrib.auth.models import User
from cards.models import Card



class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'food'),
        ('TRANSPORT', 'transport'),
        ('ENTERTAINMENT', 'entertainment'),
        ('BILLS', 'bills'),
        ('OTHER', 'other')

    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='OTHER')
    date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

    