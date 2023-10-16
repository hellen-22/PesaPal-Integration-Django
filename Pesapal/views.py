import uuid
import requests

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .utils import PesaPalGateway
from core.settings import env

payment_url = env("PAYMENT_URL")

gateway = PesaPalGateway()

def pay(request):
    if request.method == "POST":
        phonenumber = request.POST["phone_number"]
        email = request.POST["email"]
        amount = 100.00
        currency = "KES"
        callback_url = "https://e398-154-159-252-84.ngrok-free.app/callback"

        res = gateway.make_payment(phonenumber, email, amount, currency, callback_url)
        print(res)

    return render(request, 'payments.html')

def paymentIPN(request):
    orderTrackingId = request.GET.get("OrderTrackingId")
    orderMerchantReference = request.GET.get("OrderMerchantReference")
    orderNotificationType = request.GET.get("OrderNotificationType")

    payment_url = f"https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus?orderTrackingId={orderTrackingId}"

    token = gateway.getAuthorizationToken()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % token,
        "Accepts": "application/json"
    }
    payment_status = requests.get(payment_url, headers=headers)


    return JsonResponse(payment_status.json())


def callback(request):
    return HttpResponse("Successs")

