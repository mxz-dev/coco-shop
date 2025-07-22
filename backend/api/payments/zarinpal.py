import requests
from django.conf import settings

def zarinpal_payment(amount, description, email, mobile, currency="IRR"):
    marchant_id = settings.MARCHANT_ID
    callback_url = settings.CALLBACK_URL

    data = {
        "merchant_id": marchant_id,
        "amount": amount,
        "callback_url": callback_url,
        "description": description,
        "metadata": {"mobile": mobile,"email": email},
        "currency": currency
    }

    response = requests.post("https://sandbox.zarinpal.com/pg/v4/payment/request.json", data=data, headers={"accept": "application/json", "content-type": "application/json"})
    
    res_data = response.json()

    if res_data['data']['code'] == 100:
        payment_url = f"https://payment.zarinpal.com/pg/StartPay/{res_data['data']['authority']}"
        return payment_url
    else:
        Exception(f"Zarinpal error: {res_data['errors']}")


def zarinpal_verify(amount, authority):
    marchant_id = settings.MARCHANT_ID

    data = {
        "merchant_id": marchant_id,
        "amount": amount,
        "authority":authority
    }

    response = requests.post("https://sandbox.zarinpal.com/pg/v4/payment/verify.json", data=data, headers={"accept": "application/json", "content-type": "application/json"})
    res_data = response.json()
    if res_data['data']['code'] == 100 or res_data['data']['code'] == 101:
        return res_data
    else:
        Exception(f"Verify error: {res_data['errors']}")