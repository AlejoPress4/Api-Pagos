import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cargar las variables del archivo .env
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_HOST_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

def send_payment_notification(email_recipient):
    subject = "Pago Realizado con Éxito"
    body = "Su pago ha sido procesado con éxito. Gracias por su compra."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email_recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False