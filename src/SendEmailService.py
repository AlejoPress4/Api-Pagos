import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

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