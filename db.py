import sqlite3
import os


def conectar_base_datos():
    # Obtener la ruta absoluta del directorio actual
    ruta_basedatos = "base.db"

    # ruta_basedatos = os.path.join('database', 'informes.db')
    if os.path.exists(ruta_basedatos):
        try:
            # Conexión a la base de datos
            conn = sqlite3.connect(ruta_basedatos)
            print("Conexión exitosa a la base de datos SQLite")
            return conn
        except sqlite3.Error as e:
            print("Error al conectar a la base de datos SQLite:", e)
            return None
    else:
        print("La base de datos no existe.")
        return None
    
def traer_datos():
    # Obtener datos de la base de datos
    try:
        conn = conectar_base_datos()
        if conn:
            cursor = conn.cursor()
            consulta = """
                        SELECT * FROM datospc
                        """
            cursor.execute(consulta)
            
            filas = cursor.fetchall()

            return filas
    except sqlite3.Error as e:
        print("Error al consultar datos", e)


def insertardb(placaSerial,nombreEquipo,cpuFabricante,cpuSerial,procesadorNombre,procesadorVelo,procesadorSerial,
               ram1Marca,ram1Capacidad,ram1Serial,ram2Marca,ram2Capacidad,ram2Serial,discoMarca,discoCapacidad,discoSerial,unidadCd,
               unidadCDSerial,monitorMarca,monitorModelo,nombreUsuario,direccionMac):
    try:
        conn = conectar_base_datos()
        if conn:
            cursor = conn.cursor()
            consulta = """
                        INSERT INTO datospc (
                            placaSerial,nombreEquipo,cpuFabricante,cpuSerial,procesadorNombre,procesadorVelo,procesadorSerial,
                            ram1Marca,ram1Capacidad,ram1Serial,ram2Marca,ram2Capacidad,ram2Serial,discoMarca,discoCapacidad,discoSerial,unidadCd,
                            unidadCDSerial,monitorMarca,monitorModelo,nombreUsuario,direccionMac
                        ) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
            valores = (placaSerial,nombreEquipo,cpuFabricante,cpuSerial,procesadorNombre,procesadorVelo,procesadorSerial,
                        ram1Marca,ram1Capacidad,ram1Serial,ram2Marca,ram2Capacidad,ram2Serial,discoMarca,discoCapacidad,discoSerial,unidadCd,
                        unidadCDSerial,monitorMarca,monitorModelo,nombreUsuario,direccionMac)
            cursor.execute(consulta,valores)
            # Guardar los cambios
            conn.commit()
            print("Datos insertados correctamente.")
    except sqlite3.Error as e:
        print("Error al insertar datos", e)

    finally:
        # Cerrar la conexion
        conn.close()