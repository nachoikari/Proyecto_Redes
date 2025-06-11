from flask import Blueprint, jsonify
import mysql.connector
from lib.config.db_config import db_config

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial/<numero>', methods=['GET'])
def obtener_historial(numero):
    try:
        print("📥 [HISTORIAL] Número recibido:", numero)

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        print("🔍 [HISTORIAL] Consultando ID del usuario...")
        cursor.execute("SELECT idUsuario FROM Usuario WHERE usuario_numero = %s", (numero,))
        result = cursor.fetchone()

        if not result:
            print("❌ [HISTORIAL] Usuario no encontrado")
            return jsonify({"status": "ERROR", "message": "Usuario no encontrado"}), 404

        id_cliente = result["idUsuario"]
        print("✅ [HISTORIAL] ID del cliente:", id_cliente)

        # Obtener historial de transacciones
        query = """
        SELECT detalle, monto, numero_receptor, estado_transaccion, fecha_transaccion
        FROM log_transacciones
        WHERE id_cliente = %s
        ORDER BY fecha_transaccion DESC
        """
        print("🔍 [HISTORIAL] Ejecutando consulta de historial...")
        cursor.execute(query, (id_cliente,))
        historial = cursor.fetchall()

        print(f"📦 [HISTORIAL] Transacciones encontradas: {len(historial)}")
        for t in historial:
            print("    →", t)

        cursor.close()
        connection.close()

        return jsonify({
            "status": "OK",
            "historial": historial
        }), 200

    except mysql.connector.Error as e:
        print("❌ [HISTORIAL] Error MySQL:", str(e))
        return jsonify({"status": "ERROR", "message": str(e)}), 500

    except Exception as ex:
        print("❌ [HISTORIAL] Error inesperado:", str(ex))
        return jsonify({"status": "ERROR", "message": "Error inesperado en el servidor"}), 500
