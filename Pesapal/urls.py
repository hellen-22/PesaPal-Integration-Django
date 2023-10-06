from django.urls import path
from . import views

urlpatterns = [
    path('', views.pay, name='answers')
]