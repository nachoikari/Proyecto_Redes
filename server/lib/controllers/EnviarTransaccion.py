from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import mysql.connector
from lib.config.db_config import db_config
from lib.config.constants import PREFIJO_LOCAL

# Blueprint para esta sección
sinpe_bp = Blueprint('enviarSinpe', __name__)

@sinpe_bp.route('/enviar-sinpe', methods=['POST'])
@cross_origin()
def enviar_sinpe():

    try:
        data = request.get_json()
        print("=====================")
        print(data)
        print("=====================")

        num_emisor = data.get('num_emisor')
        origen = data.get('origen')           # Opcional
        destino = data.get('destino')         # Opcional
        monto = float(data.get('monto', 0))
        num_destino = data.get('num_destino')

        if not all([num_emisor, num_destino, monto]):
            return jsonify({"status": "ERROR", "message": "Faltan campos requeridos"}), 400

        prefijo_destino = int(num_destino[:2])
        print(prefijo_destino)
        if PREFIJO_LOCAL == prefijo_destino:
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor(dictionary=True)

                # Verifica que el emisor exista y tenga fondos suficientes
                cursor.execute("SELECT usuario_monto FROM Usuario WHERE usuario_numero = %s", (num_emisor,))
                emisor = cursor.fetchone()
                if not emisor:
                    return jsonify({"status": "ERROR", "message": "Emisor no existe"}), 404
                if emisor['usuario_monto'] < monto:
                    return jsonify({"status": "ERROR", "message": "Fondos insuficientes"}), 400

                # Verifica que el receptor exista
                cursor.execute("SELECT usuario_monto FROM Usuario WHERE usuario_numero = %s", (num_destino,))
                receptor = cursor.fetchone()
                if not receptor:
                    return jsonify({"status": "ERROR", "message": "Receptor no existe"}), 404

                # Realiza la transferencia
                cursor.execute("UPDATE Usuario SET usuario_monto = usuario_monto - %s WHERE usuario_numero = %s", (monto, num_emisor))
                cursor.execute("UPDATE Usuario SET usuario_monto = usuario_monto + %s WHERE usuario_numero = %s", (monto, num_destino))
                connection.commit()

                return jsonify({"status": "OK", "message": "Transferencia completada"}), 200

            except mysql.connector.Error as e:
                return jsonify({"status": "ERROR", "message": str(e)}), 500

            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({"status": "ERROR", "message": "Transacción externa no implementada aún"}), 501

    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error inesperado: {str(e)}"}), 500
