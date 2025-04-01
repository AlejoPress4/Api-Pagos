from flask import Blueprint, request, jsonify
from services.epayco_service import create_payment
from services.mail_service import send_payment_notification

# Crear el Blueprint para las rutas de pago
payment_routes = Blueprint('payment_routes', __name__)

@payment_routes.route('/payment', methods=['POST'])
def process_payment():
    data = request.json
    email = data.get('email')
    amount = data.get('amount')
    currency = data.get('currency', 'USD')  # Moneda por defecto: USD
    description = data.get('description', 'Payment description')  # Descripción por defecto

    # Validar que los campos requeridos estén presentes
    if not email or not amount:
        return jsonify({'error': 'Email and amount are required'}), 400

    # Crear el pago usando el servicio de ePayco
    payment_response = create_payment(amount, currency, description, email)

    if payment_response.get('status') == 'success':
        # Enviar notificación por correo
        email_sent = send_payment_notification(email)
        if email_sent:
            return jsonify({'message': 'Payment processed successfully', 'payment_info': payment_response}), 200
        else:
            return jsonify({'error': 'Payment processed, but email notification failed'}), 500
    else:
        return jsonify({'error': 'Payment processing failed', 'details': payment_response}), 500