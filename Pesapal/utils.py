import requests
import logging
import uuid

from core.settings import env

class PesaPalGateway:
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    payment_url = None
    notification_id = None
    register_ipn_url = None

    def __init__(self):
        self.consumer_key = env("CONSUMER_KEY")
        self.consumer_secret = env("CONSUMER_SECRET")
        self.access_token_url = env("ACCESS_TOKEN_URL")
        self.payment_url = env("PAYMENT_URL")
        self.notification_id = env("NOTIFICATION_ID")
        self.register_ipn_url = env("REGISTER_IPN_URL")


    def getAuthorizationToken(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }

        try:
            res = requests.post(self.access_token_url, headers=headers, json=payload)

        except Exception as err:
            logging.error("Error {}".format(err))

        else:
            token = res.json()["token"]
            return token
    
    def get_notification_id(self):
        token = self.getAuthorizationToken()
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer %s" % token
        }

        payload = {
            "url": "https://e398-154-159-252-84.ngrok-free.app/payment-ipn",
            "ipn_notification_type": "GET"
        }

        try:
            res = requests.post(self.register_ipn_url, headers=headers, json=payload)
            print(res.json())

            notification_id =  res.json()["ipn_id"]

            return notification_id

        except Exception as err:
            logging.error("Error {}".format(err))

        

    def make_payment(self, phonenumber, email, amount, currency, callback_url):
        token = self.getAuthorizationToken()

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % token
        }

        data = {
            "id": str(uuid.uuid4()),
            "currency": currency,
            "amount": amount,
            "description": "Payment to Maasaibeads",
            "callback_url": callback_url,
            "notification_id": self.get_notification_id(),
            "billing_address": {
                "phone_number": phonenumber,
                "email_address": email,
            }
        }

        try:
            res = requests.post(self.payment_url, headers=headers, json=data)
            response = res.json()

            return response
        except:
            raise Exception("An error occured")

        