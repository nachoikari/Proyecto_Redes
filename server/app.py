from flask import Flask
from flask_cors import CORS

# Importar blueprint del controlador de login
from lib.controllers.LoginController import login_bp
from lib.controllers.EnviarTransaccion import sinpe_enviar_bp
from lib.controllers.RecibirSinpe import sinpe_recibir_bp
from lib.controllers.UsuarioController import usuario_bp
app = Flask(__name__)

CORS(app, origins="*", allow_headers="*", supports_credentials=True)
# Registrar los blueprints (rutas)
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(sinpe_enviar_bp, url_prefix='/api')
app.register_blueprint(sinpe_recibir_bp, url_prefix='/api')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
    
