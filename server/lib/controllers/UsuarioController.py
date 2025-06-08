from flask import Blueprint, jsonify
import mysql.connector
from lib.config.db_config import db_config

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuario/<numero>', methods=['GET'])
def obtener_usuario(numero):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT usuario_cedula, usuario_nombre, usuario_primer_apellido, usuario_numero, usuario_monto
        FROM Usuario
        WHERE usuario_numero = %s
        """
        cursor.execute(query, (numero,))
        usuario = cursor.fetchone()

        cursor.close()
        connection.close()

        if usuario:
            return jsonify({
                "status": "OK",
                "usuario": {
                    "cedula": usuario["usuario_cedula"],
                    "nombre": usuario["usuario_nombre"],
                    "apellido": usuario["usuario_primer_apellido"],
                    "numero": usuario["usuario_numero"],
                    "monto": float(usuario["usuario_monto"])
                }
            }), 200
        else:
            return jsonify({"status": "ERROR", "message": "Usuario no encontrado"}), 404

    except mysql.connector.Error as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
