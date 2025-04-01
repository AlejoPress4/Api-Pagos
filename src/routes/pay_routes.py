from flask import Blueprint, request, jsonify
from services.epayco_service import create_payment
from services.email_service import send_payment_notification

payment_routes = Blueprint('payment_routes', name)

@payment_routes.route('/payment', methods=['POST'])
def process_payment():
    data = request.json
    email = data.get('email')
    amount = data.get('amount')

    if not email or not amount:
        return jsonify({'error': 'Email and amount are required'}), 400

    payment_response = create_payment(amount)

    if payment_response['status'] == 'success':
        send_payment_notification(email, amount)
        return jsonify({'message': 'Payment processed successfully', 'payment_info': payment_response}), 200
    else:
        return jsonify({'error': 'Payment processing failed', 'details': payment_response}), 500