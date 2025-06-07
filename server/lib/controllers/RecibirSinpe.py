from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from lib.config.db_config import db_config
from lib.utils.db_utils import get_connection, close_connection, get_usuario_monto, actualizar_monto, get_id_usuario, registrar_log_transaccion
from datetime import datetime
from lib.config.constants import PREFIJO_LOCAL, API_KEY_URL, KEY_EMISOR
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
        num_destino = data.get('num_destino')
        monto = float(data.get('monto', 0))
        detalle = data.get('detalle', '')
        key_emisor = data.get('key_emisor', '')
        fecha = data.get('fecha', '')

        # Validar campos requeridos
        if not all([num_emisor, num_destino, monto, key_emisor, fecha]):
            return jsonify({"status": "ERROR", "message": "Faltan datos requeridos"}), 400
        try:
            fecha_convertida = datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            return jsonify({"status": "ERROR", "message": "Formato de fecha inválido"}), 400
        
        prefijo_emisor = int(num_emisor[:2])
        
        api_key_url = f"{API_KEY_URL}{prefijo_emisor}"
        
        response = requests.get(api_key_url, verify=False)
        
        if response.status_code != 200:
             return jsonify({"status": "ERROR", "message": "No se pudo obtener información del banco destino"}), 400
        connection, cursor = get_connection()

        receptor = get_usuario_monto(cursor, num_destino)
        
        if not receptor:
            close_connection(connection, cursor)
            return jsonify({"status": "ERROR", "message": "Receptor no existe"}), 404

        actualizar_monto(cursor, num_destino, monto, operacion='+')
        id_receptor = get_id_usuario(cursor, num_destino)
        registrar_log_transaccion(cursor,detalle=detalle,numero_emisor=num_emisor,numero_receptor=num_destino,id_cliente=id_receptor,fecha=fecha_convertida,estado="COMPLETADA: RECEPCIÓN EXTERNA")
        connection.commit()
        close_connection(connection, cursor)

        print(f"✅ Se acreditaron ₡{monto} al usuario {num_destino} de parte de {num_emisor}. Detalle: {detalle}")
        return jsonify({"status": "OK", "message": "Transacción recibida correctamente"}), 200

    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error inesperado: {str(e)}"}), 500
