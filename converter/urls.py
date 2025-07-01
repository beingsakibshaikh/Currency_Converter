from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('convert/', views.convert_currency, name='convert_currency'),
    
]
