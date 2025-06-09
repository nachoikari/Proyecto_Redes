from flask import Blueprint, jsonify
import mysql.connector
from lib.config.db_config import db_config

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial/<numero>', methods=['GET'])
def obtener_historial(numero):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Obtener el idUsuario (no id_usuario) del número de teléfono
        cursor.execute("SELECT idUsuario FROM Usuario WHERE usuario_numero = %s", (numero,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"status": "ERROR", "message": "Usuario no encontrado"}), 404

        id_cliente = result["idUsuario"]

        # Obtener el historial de transacciones para ese cliente
        query = """
        SELECT detalle, monto, numero_receptor, estado_transaccion, fecha_transaccion
        FROM log_transacciones
        WHERE id_cliente = %s
        ORDER BY fecha_transaccion DESC
        """
        cursor.execute(query, (id_cliente,))
        historial = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "status": "OK",
            "historial": historial
        }), 200

    except mysql.connector.Error as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
