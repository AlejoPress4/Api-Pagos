from flask import Flask
from src.routes.pay_routes import payment_routes
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Registrar las rutas de pago
app.register_blueprint(payment_routes)

if __name__ == '__main__':
    # Puedes acceder a las variables de entorno con os.getenv
    app.run(debug=True, host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"), port=int(os.getenv("FLASK_RUN_PORT", 5500)))