from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),
    path('expenses/', include('expenses.urls')),
    path('budgets/', include('budgets.urls')),
    path('cards/', include('cards.urls'))
]
