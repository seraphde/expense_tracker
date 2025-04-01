# budgets/urls.py
from django.urls import path
from .views import budget_list_create, budget_detail, budgets_progress  

urlpatterns = [
    path('budgets/', budget_list_create, name='budget_list_create'),
    path('budgets/<int:pk>/', budget_detail, name='budget_detail'),
    path('budgets/<int:pk>/progress/', budgets_progress, name='budgets_progress'),
      
]

