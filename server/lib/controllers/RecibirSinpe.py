from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from lib.config.db_config import db_config
from lib.utils.db_utils import get_connection, close_connection, get_usuario_monto, actualizar_monto, get_id_usuario, registrar_log_transaccion
from datetime import datetime
from lib.config.constants import PREFIJO_LOCAL, API_KEY_URL, KEY_EMISOR
import requests

sinpe_recibir_bp = Blueprint('recibirSinpe', __name__)

@sinpe_recibir_bp.route('/recibir-sinpe', methods=['POST'])
@cross_origin()
def recibir_sinpe():
    try:
        data = request.get_json()
        print("======= TRANSACCIÓN RECIBIDA =======")
        print(data)
        print("====================================")

        num_emisor = data.get('num_emisor')
        num_destino = data.get('num_receptor')
        monto = float(data.get('monto', 0))
        detalle = data.get('detalle', '')
        key_emisor = data.get('key_emisor', '')

        print(f"[INFO] num_emisor: {num_emisor}, num_receptor: {num_destino}, monto: {monto}, detalle: {detalle}, key_emisor: {key_emisor}")

        if not all([num_emisor, num_destino, monto, key_emisor]):
            print("[ERROR] Faltan datos requeridos")
            return jsonify({"status": "ERROR", "message": "Faltan datos requeridos"}), 500

        prefijo_emisor = num_emisor[:2]
        print(f"[INFO] Prefijo emisor: {prefijo_emisor}")

        api_key_url = f"{API_KEY_URL}{prefijo_emisor}"
        print(f"[INFO] Consultando API KEY URL: {api_key_url}")
        
        response = requests.get(api_key_url, verify=False)
        print(f"[INFO] Respuesta de API KEY URL: {response.status_code}, body: {response.text}")

        if response.status_code != 200:
            print("[ERROR] No se pudo obtener información del banco destino")
            return jsonify({"status": "ERROR", "message": "No se pudo obtener información del banco destino"}), 500

        print("[INFO] Abriendo conexión a base de datos...")
        connection, cursor = get_connection()

        print(f"[INFO] Buscando receptor {num_destino}...")
        receptor = get_usuario_monto(cursor, num_destino)

        if not receptor:
            print("[ERROR] Receptor no existe")
            close_connection(connection, cursor)
            return jsonify({"status": "ERROR", "message": "Receptor no existe"}), 500

        print("[INFO] Receptor encontrado, actualizando monto...")
        actualizar_monto(cursor, num_destino, monto, operacion='+')

        print("[INFO] Obteniendo ID del receptor...")
        id_receptor = get_id_usuario(cursor, num_destino)

        print("[INFO] Registrando transacción en log...")
        fecha_convertida = datetime.today().strftime("%Y-%m-%d")
        print(f"[INFO] Fecha actual: {fecha_convertida}")

        registrar_log_transaccion(
            cursor,
            detalle=detalle,
            numero_emisor=num_emisor,
            numero_receptor=num_destino,
            id_cliente=id_receptor,
            fecha=fecha_convertida,
            monto=monto,
            estado="COMPLETADA: RECEPCIÓN EXTERNA"
        )

        print("[INFO] Commit de la transacción...")
        connection.commit()
        close_connection(connection, cursor)

        print(f"✅ Se acreditaron ₡{monto} al usuario {num_destino} de parte de {num_emisor}. Detalle: {detalle}")
        return jsonify({"status": "OK", "message": "Transacción recibida correctamente"}), 200

    except Exception as e:
        print(f"[ERROR] Excepción inesperada: {str(e)}")
        return jsonify({"status": "ERROR", "message": f"Error inesperado: {str(e)}"}), 400
