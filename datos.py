import csv
from db import *

def buscar(archivo, lugar, palabra):
    encontrado = False  # Bandera para controlar si se encuentra el lugar especificado
    with open(archivo, newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            if encontrado:  # Si ya se encontró el lugar especificado
                if len(fila) > 0 and palabra in fila[0]:  # Verifica si la palabra está en la primera columna
                    return fila
            elif lugar in fila:  # Si encuentra el lugar especificado
                encontrado = True
    return None  # Si no se encuentra el lugar o la palabra, devuelve None


# funcion que busca una palabra en todo el documento sin importar si conicide exactamente o no
def buscar_en_csv(archivo, palabra):
    with open(archivo, newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            for celda in fila:
                if palabra.lower() in celda.lower():
                    return fila
    return None  # Si no se encuentra la palabra, devuelve None

def validar(dato):
    if dato != None:
        if len(dato[1]) > 1 and dato[1]: 
            return str(dato[1])
        else:
            return "No se encontro"
    else:
        return "No se encontro"
    


# Ejemplo de uso
archivo_csv = 'portatilrespiratoria.csv'
# archivo_csv = 'Facturacion todo en uno hp negro.csv'

# DATOS DEL CHASIS DEL COMPUTADOR
# Nombre del fabricante
FabricateCaja = buscar(archivo_csv,"Caja del sistema","Fabricante")
FabricateCaja = validar(FabricateCaja)
# Numero de serie 
SerieCaja = buscar(archivo_csv,"Caja del sistema","Número de serie:")
SerieCaja = validar(SerieCaja)
# Placa de la cpu (Generada por inventario)
placaCaja = None

# DATOS DEL PROCESADOR
# Nombre del procesador
nombreCPU = buscar(archivo_csv,"Procesador","Processor Version:")
nombreCPU = validar(nombreCPU)
# Velocidad del procesador
velocidadCPU = buscar(archivo_csv,"Procesador","Frecuencia actual:")
velocidadCPU = validar(velocidadCPU)
# ID del procesador
idCPU = buscar(archivo_csv,"Procesador(es) central","CPU ID:")
idCPU = validar(idCPU)

# DATOS DE LA MEMORIA RAM
# Datos modulo ram 1
ram1Capacidad = buscar(archivo_csv,"Matriz de memoria física","Tamaño del dispositivo:")
ram1Capacidad = validar(ram1Capacidad)
ram1Marca = buscar(archivo_csv,"Bank Locator:","Fabricante:")
ram1Marca = validar(ram1Marca)
ram1Serial = buscar(archivo_csv,"Bank Locator:","Número de serie:")
ram1Serial = validar(ram1Serial)
# Datos modulo ram 2
ram2Capacidad = buscar(archivo_csv,"Bank Locator:","Tamaño del dispositivo:")
print(ram2Capacidad)
ram2Capacidad = validar(ram2Capacidad)
ram2Marca = buscar(archivo_csv,"BANK 1","Fabricante:")
ram2Marca = validar(ram2Marca)
ram2Serial = buscar(archivo_csv,"BANK 1","Número de serie:")
ram2Serial = validar(ram2Serial)

# INFORMACION DEL DISCO
discoMarca = buscar(archivo_csv,"Unidades de disco","Modelo de unidad:")
discoMarca = validar(discoMarca)
discoCapacidad = buscar(archivo_csv,"Unidades de disco","Capacidad de la unidad:")
discoCapacidad = validar(discoCapacidad)
discoSerial = buscar(archivo_csv,"Unidades de disco","Número de serie de la unidad:")
discoSerial = validar(discoSerial)

# UNIDAD DE CD
# busco la palabra en todo el documento, la paso a string y tomo el valor ubicado en la posicion 0
bandera = buscar_en_csv(archivo_csv, "DVD")
if bandera != None:
    # Si entra encontro algo
    bandera = str(bandera[0])
    unidadDVD = buscar(archivo_csv,bandera,"Modelo de unidad:")
    unidadDVD = validar(unidadDVD)
    serialDVD = buscar(archivo_csv,bandera,"Número de serie:")
    serialDVD = validar(serialDVD)
else:
    # No encontro nada
    unidadDVD = "No se encontro"
    serialDVD = "No se encontro"

# MONITOR
monitorMarca = buscar(archivo_csv,"Monitor","Nombre del monitor (del fabricante):")
monitorMarca = validar(monitorMarca)
monitorModelo = buscar(archivo_csv,"Monitor","Nombre del monitor (del fabricante):")
monitorModelo = validar(monitorModelo)

# Nombre de usuario del equipo
nombreEquipo = str(buscar_en_csv(archivo_csv,"Nombre del computadora:")[1])
usuario = buscar(archivo_csv,"Nombre del computadora:","Nombre de usuario actual:")
usuario = validar(usuario)

# Direccion MAC
direccionMAC = str(buscar_en_csv(archivo_csv,"Ethernet")[0])
direccionMAC = buscar(archivo_csv,direccionMAC,"Dirección MAC:")
direccionMAC = validar(direccionMAC)

# Numero de serie de la placa madre
placaSerial = buscar(archivo_csv,"tarjeta madre","Número de serie de la placa base:")
placaSerial = validar(placaSerial)

insertardb(placaSerial,nombreEquipo,FabricateCaja,SerieCaja,nombreCPU,velocidadCPU,idCPU,
               ram1Marca,ram1Capacidad,ram1Serial,ram2Marca,ram2Capacidad,ram2Serial,discoMarca,discoCapacidad,discoSerial,unidadDVD,
               unidadDVD,monitorMarca,monitorModelo,usuario,direccionMAC)