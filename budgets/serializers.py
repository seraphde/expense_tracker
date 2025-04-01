from rest_framework import serializers
from . models import Budget

class BudgetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'