from django.urls import path
from . import views

urlpatterns = [
    path('', views.pay, name='answers'),
    path('payment-ipn', views.paymentIPN, name="payment-ipn"),
    path('callback', views.callback, name='callback')
]