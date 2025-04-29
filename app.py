from flask import Flask, request, jsonify
from dotenv import load_dotenv
import epaycosdk.epayco as epayco
import json
import os
import requests


# Cargar variables de entorno
load_dotenv()

# Configuración de Epayco
apiKey = os.getenv("PUBLIC_KEY")
privateKey = os.getenv("PRIVATE_KEY")
lenguage = "ES"
test = True  # Cambiar a False en producción
options = {"apiKey": apiKey, "privateKey": privateKey, "test": test, "lenguage": lenguage}

# Inicializar cliente de Epayco
objepayco = epayco.Epayco(options)

# Inicializar aplicación Flask
app = Flask(__name__)

def send_email(email, bill, charge_details):
    """
    Función para enviar un correo al cliente con los detalles de la factura usando el servicio de notificaciones.
    """
    try:
        # Obtener la URL del servicio de notificaciones del archivo .env
        notification_url = os.getenv('NOTIFICATION_SERVICE_URL')

        # Preparar los datos para enviar al servicio de notificaciones
        email_data = {
            "recipient": email,
            "message": f"""
            Gracias por tu pago. Aquí están los detalles de tu factura:

            Número de factura: {bill}
            Valor: {charge_details['data']['valor']}
            Descripción: {charge_details['data']['descripcion']}
            Estado: {charge_details['data']['estado']}
            Respuesta: {charge_details['data']['respuesta']}

            Si tienes alguna pregunta, no dudes en contactarnos.

            Saludos,
            Tu Empresa
            """,
            "subject": f"Factura {bill} - Detalles del Pago"
        }

        # Hacer la petición al servicio de notificaciones
        response = requests.post(notification_url, json=email_data)
        
        if response.status_code == 200:
            print(f"Notificación de pago enviada exitosamente a {email}")
            return True
        else:
            print(f"Error al enviar la notificación: {response.json()}")
            return False

    except Exception as e:
        print(f"Error al conectar con el servicio de notificaciones: {e}")
        return False

@app.route('/charge', methods=['POST'])
def charge():
    try:
        # Obtener datos del cliente y de la tarjeta desde el cuerpo de la solicitud
        data = request.get_json()
        print("Datos recibidos:", data)

        # Generar token de la tarjeta
        token_card = objepayco.token.create({
            "card[number]": data['card']['number'],
            "card[exp_year]": data['card']['exp_year'],
            "card[exp_month]": data['card']['exp_month'],
            "card[cvc]": data['card']['cvc'],
            "hasCvv": True
        })
        print("Token generado:", token_card)

        if not token_card.get('status', False):
            return jsonify({"error": "Error al generar el token", "details": token_card}), 400

        # Crear cliente en Epayco
        customer = objepayco.customer.create({
            "token_card": token_card['id'],
            "name": data['customer']['name'],
            "last_name": data['customer']['last_name'],
            "email": data['customer']['email'],
            "phone": data['customer']['phone'],
            "default": True
        })
        print("Cliente creado:", customer)

        if not customer.get('status', False):
            return jsonify({"error": "Error al crear el cliente", "details": customer}), 400

        customer_id = customer['data']['customerId']

        # Preparar información de pago
        payment_info = {
            "token_card": token_card['id'],
            "customer_id": customer_id,
            "doc_type": "CC",
            "doc_number": data['customer']['doc_number'],
            "name": data['customer']['name'],
            "last_name": data['customer']['last_name'],
            "email": data['customer']['email'],
            "bill": data['bill'],
            "description": data['description'],
            "value": int(data['value']),
            "tax": int(data['tax']),
            "tax_base": int(data['tax_base']),
            "currency": "COP",
            "dues": data['dues'],
            "ip": "190.000.000.000",
            "url_response": "https://tudominio.com/respuesta.php",
            "url_confirmation": "https://tudominio.com/confirmacion.php",
            "method_confirmation": "GET",
            "use_default_card_customer": True,
        }

        # Crear cargo
        charge = objepayco.charge.create(payment_info)
        print("Respuesta de Epayco (cargo):", charge)

        if not charge.get('status', False):
            return jsonify({"error": "Error en el cargo", "details": charge}), 400

        # Enviar correo al cliente con los detalles de la factura
        email_sent = send_email(data['customer']['email'], data['bill'], charge)

        # Formatear la respuesta
        response = {
            "message": "Pago procesado" + (" y correo enviado" if email_sent else " (error al enviar correo)"),
            "details": charge
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error procesando la solicitud: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)