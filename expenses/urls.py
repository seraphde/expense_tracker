from django.urls import path
from .views import expense_list_create, expense_detail, login_page, logout_page, register_user, weekly_summary, monthly_summary
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [ 
    path('expenses/', expense_list_create, name='expense_list_create'),
    path('expenses/<int:pk>/', expense_detail, name='expense_detail'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('api/register/', register_user, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('expenses/weekly-summary/', weekly_summary, name='weekly-summary'),
    path('expenses/monthly-summary/', monthly_summary, name='monthly-summary'),
    
]
 