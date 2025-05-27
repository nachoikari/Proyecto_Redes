from flask import Flask
from flask_cors import CORS

# Importar blueprint del controlador de login
from lib.controllers.LoginController import login_bp

app = Flask(__name__)
CORS(app)  # Permite peticiones desde React u otros orígenes

# Registrar los blueprints (rutas)
app.register_blueprint(login_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
