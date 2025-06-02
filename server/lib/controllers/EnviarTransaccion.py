from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import mysql.connector
from lib.config.db_config import db_config
from lib.config.constants import PREFIJO_LOCAL, API_KEY_URL
import requests
import datetime
from lib.utils.db_utils import get_connection, close_connection, get_usuario_monto, actualizar_monto, get_id_usuario, registrar_log_transaccion

sinpe_enviar_bp = Blueprint('enviarSinpe', __name__)

@sinpe_enviar_bp.route('/enviar-sinpe', methods=['POST'])
@cross_origin()
def enviar_sinpe():
    try:
        data = request.get_json()
        print("=====================")
        print(data)
        print("=====================")

        num_emisor = data.get('num_emisor')
        monto = float(data.get('monto', 0))
        num_destino = data.get('num_destino')
        detalle = data.get('detalle', 'Sin detalle')
        key_emisor = data.get('key_emisor', '')
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")

        if not all([num_emisor, num_destino, monto, key_emisor]):
            return jsonify({"status": "ERROR", "message": "Faltan campos requeridos"}), 400

        prefijo_destino = int(num_destino[:2])

        if PREFIJO_LOCAL == prefijo_destino:
            connection, cursor = None, None
            try:
                connection, cursor = get_connection()

                emisor = get_usuario_monto(cursor, num_emisor)

                if not emisor:
                    close_connection(connection, cursor)
                    return jsonify({"status": "ERROR", "message": "Emisor no existe"}), 404
                if emisor['usuario_monto'] < monto:
                    close_connection(connection, cursor)
                    return jsonify({"status": "ERROR", "message": "Fondos insuficientes"}), 400

                receptor = get_usuario_monto(cursor, num_destino)
                if not receptor:
                    close_connection(connection, cursor)
                    return jsonify({"status": "ERROR", "message": "Receptor no existe"}), 404

                actualizar_monto(cursor, num_emisor, monto, operacion='-')
                actualizar_monto(cursor, num_destino, monto, operacion='+')
                
                # Obtener IDs
                id_emisor = get_id_usuario(cursor, num_emisor)
                id_receptor = get_id_usuario(cursor, num_destino)

                # Registrar logs
                registrar_log_transaccion(cursor, detalle, num_emisor, num_destino, id_emisor, fecha, "COMPLETADA: ENVÍO INTERNO")
                registrar_log_transaccion(cursor, detalle, num_emisor, num_destino, id_receptor, fecha, "COMPLETADA: RECEPCIÓN INTERNA")
                
                connection.commit()
                close_connection(connection, cursor)
                return jsonify({"status": "OK", "message": "Transferencia completada"}), 200

            except mysql.connector.Error as e:
                return jsonify({"status": "ERROR", "message": str(e)}), 500

            finally:
                if connection and cursor:
                    close_connection(connection, cursor)

        else:
            try:
                # Paso 1: Obtener información del banco destino
                api_key_url = f"{API_KEY_URL}{prefijo_destino}"
                response = requests.get(api_key_url, verify=False)
                if response.status_code != 200:
                    return jsonify({"status": "ERROR", "message": "No se pudo obtener información del banco destino"}), 400

                banco_info = response.json()
                endpoint_url = f"https://{banco_info['ip']}:{banco_info['puerto']}/{banco_info['endpoint']}"

                # Paso 2: Preparar cuerpo
                body = {
                    "num_emisor": num_emisor,
                    "key_emisor": key_emisor,
                    "num_receptor": num_destino,
                    "monto": monto,
                    "detalle": detalle,
                    "fecha": fecha
                }

                # Paso 3: Enviar solicitud
                response_ext = requests.post(endpoint_url, json=body, verify=False)
                respuesta_receptor = response_ext.json()

                if response_ext.status_code == 200 and respuesta_receptor.get("status") == "OK":
                    # Confirmado por el receptor → actualizamos base local (rebajo al emisor)
                    connection, cursor = get_connection()
                    actualizar_monto(cursor, num_emisor, monto, operacion='-')
                    id_cliente = get_id_usuario(cursor, num_emisor)
                    registrar_log_transaccion(cursor, detalle, num_emisor, num_destino, id_cliente, fecha, "COMPLETADA: EXITOSA")
                    connection.commit()
                    close_connection(connection, cursor)

                    return jsonify({
                        "status": "OK",
                        "message": "Transferencia completada con banco externo",
                        "respuesta": respuesta_receptor
                    }), 200
                else:
                    connection, cursor = get_connection()
                    id_cliente = get_id_usuario(cursor, num_emisor)
                    registrar_log_transaccion(cursor, detalle, num_emisor, num_destino, id_cliente, fecha, "ERROR: TRANSACCION RECHAZA")
                    connection.commit()
                    close_connection(connection, cursor)
                    return jsonify({
                        "status": "ERROR",
                        "message": "El banco receptor rechazó la transacción",
                        "respuesta": respuesta_receptor
                    }), response_ext.status_code

            except requests.RequestException as e:
                return jsonify({
                    "status": "ERROR",
                    "message": f"Fallo al contactar API central o banco destino: {str(e)}"
                }), 500

    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error inesperado: {str(e)}"}), 500
