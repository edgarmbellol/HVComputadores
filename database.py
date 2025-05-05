# app/database.py
# En este archivo se pasaran las consultas a la base de datos
import pyodbc
from config import SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD

def obtener_conexion():
    conn_str = (
        f'DRIVER={{SQL Server}};'
        f'SERVER={SQL_SERVER};'
        f'DATABASE={SQL_DATABASE};'
        f'UID={SQL_USERNAME};'
        f'PWD={SQL_PASSWORD};'
    )
    return pyodbc.connect(conn_str)

# FUNCIONES PARA CONEXION CON INVETARIOS URGENCIAS
def validar_usuario(usuario, clave):
    conn = None
    clave = clave.upper()
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerUsuario ?", (usuario,))
        row = cursor.fetchone()
        contra = ''
        print(row)
        
        if row is None:
            valor = "Error"
        else:
            for car in row[1]:
                c = ord(car) - 2
                contra = contra + chr(c)
            contra = contra.upper()
            if contra == clave:
                valor = row[2]
            else:
                valor = "Error"
        return valor
    finally:
        if conn:
            conn.close()  # Asegurarse de cerrar la conexión en todo caso





