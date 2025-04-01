from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} Budget: ${self.amount} ({self.start_date} to {self.end_date})"
    
    