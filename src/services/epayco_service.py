import os
from dotenv import load_dotenv
import requests

# Cargar las variables del archivo .env
load_dotenv()

E_PAYCO_PUBLIC_KEY = os.getenv("API_KEY")
E_PAYCO_PRIVATE_KEY = os.getenv("PRIVATE_KEY")
API_ENDPOINT = os.getenv("API_ENDPOINT")

def create_payment(amount, currency, description, email):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {E_PAYCO_PRIVATE_KEY}"
    }
    data = {
        "public_key": E_PAYCO_PUBLIC_KEY,
        "amount": amount,
        "currency": currency,
        "description": description,
        "email": email,
        "test": True  # Set to True for testing purposes
    }
    
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Payment creation failed", "details": response.json()}