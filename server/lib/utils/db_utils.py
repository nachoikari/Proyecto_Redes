import mysql.connector
from lib.config.db_config import db_config


def get_connection():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    return connection, cursor

def close_connection(connection, cursor):
    try:
        cursor.close()
        connection.close()
    except:
        pass

def get_usuario_monto(cursor, numero):
    cursor.execute("SELECT usuario_monto FROM Usuario WHERE usuario_numero = %s", (numero,))
    return cursor.fetchone()

def actualizar_monto(cursor, numero, monto, operacion='+'):
    signo = '+' if operacion == '+' else '-'
    cursor.execute(
        f"UPDATE Usuario SET usuario_monto = usuario_monto {signo} %s WHERE usuario_numero = %s",
        (monto, numero)
    )

def get_id_usuario(cursor, numero):
    cursor.execute("SELECT idUsuario, usuario_monto FROM Usuario WHERE usuario_numero = %s", (numero,))
    result = cursor.fetchone()
    return result['idUsuario'] if result else None

def registrar_log_transaccion(cursor, detalle, numero_emisor, numero_receptor, id_cliente, fecha, estado):
    query = """
        INSERT INTO log_transacciones 
        (detalle, numero_emisor, numero_receptor, id_cliente, fecha_transaccion, estado_transaccion)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (detalle, numero_emisor, numero_receptor, id_cliente, fecha, estado)
    cursor.execute(query, values)