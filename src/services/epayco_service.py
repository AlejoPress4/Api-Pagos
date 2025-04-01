from flask import request, jsonify
import requests
from src.config.settings import E_PAYCO_PUBLIC_KEY, E_PAYCO_PRIVATE_KEY

def create_payment(amount, currency, description, email):
    url = "https://api.epayco.co/payment/create/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "public_key": E_PAYCO_PUBLIC_KEY,
        "private_key": E_PAYCO_PRIVATE_KEY,
        "amount": amount,
        "currency": currency,
        "description": description,
        "email": email,
        "test": True  # Set to True for testing purposes
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Payment creation failed", "details": response.json()}

def verify_payment(token):
    url = "https://api.epayco.co/payment/verify/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "public_key": E_PAYCO_PUBLIC_KEY,
        "token": token
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Payment verification failed", "details": response.json()}