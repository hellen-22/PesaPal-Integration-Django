import uuid
import requests

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .utils import PesaPalGateway
from core.settings import env

payment_url = env("PAYMENT_URL")

gateway = PesaPalGateway()

def pay(request):
    phonenumber = "0715111575"
    email = "hellenwain@gmail.com"
    amount = 100.00
    currency = "KE"
    callback_url = "https://maasaibeads.com/"

    res = gateway.make_payment(phonenumber, email, amount, currency, callback_url)

    print(res)

    return JsonResponse(res)