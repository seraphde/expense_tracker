from django.urls import path
from .views import card_list_create, card_detail

urlpatterns = [
    path('cards/', card_list_create, name='card-list-create'),
    path('cards/<int:pk>/', card_detail, name='card-detail'),
]