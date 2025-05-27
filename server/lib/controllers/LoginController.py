from flask import Blueprint, request, jsonify
import mysql.connector
from lib.config.db_config import db_config  # 👈 Importación limpia

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cedula = data.get('cedula')
    password = data.get('password')

    if not cedula or not password:
        return jsonify({'error': 'Faltan campos'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM Usuario
        WHERE usuario_cedula = %s AND usuario_password = %s
        """
        cursor.execute(query, (cedula, password))
        usuario = cursor.fetchone()

        cursor.close()
        connection.close()

        if usuario:
            return jsonify({
                'status': 'OK',
                'usuario': {
                    'cedula': usuario['usuario_cedula'],
                    'nombre': usuario['usuario_nombre'],
                    'apellido': usuario['usuario_primer_apellido'],
                    'numero': usuario['usuario_numero'],
                    'monto': float(usuario['usuario_monto'])
                }
            }), 200
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
