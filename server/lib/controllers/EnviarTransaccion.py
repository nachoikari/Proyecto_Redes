from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import mysql.connector
from lib.config.db_config import db_config
from lib.config.constants import PREFIJO_LOCAL, API_KEY_URL
import requests
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
        destino = data.get('destino')         #Esto debe existir en caso de enviar la un sinpe a otro banco distinto
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

                cursor.execute("SELECT usuario_monto FROM Usuario WHERE usuario_numero = %s", (num_emisor,))
                emisor = cursor.fetchone()
                
                if not emisor:
                    return jsonify({"status": "ERROR", "message": "Emisor no existe"}), 404
                if emisor['usuario_monto'] < monto:
                    return jsonify({"status": "ERROR", "message": "Fondos insuficientes"}), 400

                cursor.execute("SELECT usuario_monto FROM Usuario WHERE usuario_numero = %s", (num_destino,))
                receptor = cursor.fetchone()
                if not receptor:
                    return jsonify({"status": "ERROR", "message": "Receptor no existe"}), 404

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
            try:
                api_key_url = f"{API_KEY_URL}{prefijo_destino}"
                response = requests.get(api_key_url, verify=False) 

                print("======= RESPUESTA DE LA API CENTRAL =======")
                print("Código de estado:", response.status_code)
                print("Contenido:", response.text)
                print("===========================================")

                return jsonify({
                    "status": "DEBUG",
                    "mensaje": "Respuesta recibida de la API central",
                    "respuesta": response.json()
                }), 200

            except requests.RequestException as e:
                return jsonify({
                    "status": "ERROR",
                    "message": f"Fallo al contactar API central: {str(e)}"
                }), 500

    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error inesperado: {str(e)}"}), 500
