from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import database as citisalud
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from reporte import crear_hoja_vida
from reporte_pdf import crear_hoja_vida_pdf
from sqlalchemy import func
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sopo2025*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Datospc(db.Model):
    __tablename__ = 'datospc'
    
    placaSerial = db.Column(db.String(50))
    responsable = db.Column(db.String(100))
    Ubicacion = db.Column(db.String(100))
    Sede = db.Column(db.String(100))
    nombreEquipo = db.Column(db.String(100))
    cpuFabricante = db.Column(db.String(100))
    cpuSerial = db.Column(db.String(100))
    cpuPlaca = db.Column(db.String(100))
    procesadorNombre = db.Column(db.String(100))
    procesadorVelo = db.Column(db.String(100))
    procesadorSerial = db.Column(db.String(100))
    ram1Marca = db.Column(db.String(100))
    ram1capacidad = db.Column(db.String(100))
    ram1Serial = db.Column(db.String(100))
    ram2Marca = db.Column(db.String(100))
    ram2Capacidad = db.Column(db.String(100))
    ram2Serial = db.Column(db.String(100))
    discoMarca = db.Column(db.String(100))
    discoCapacidad = db.Column(db.String(100))
    discoSerial = db.Column(db.String(100))
    unidadCD = db.Column(db.String(100))
    unidadCDSerial = db.Column(db.String(100))
    monitorMarca = db.Column(db.String(100))
    monitorModelo = db.Column(db.String(100))
    monitorSerial = db.Column(db.String(100))
    monitorPlaca = db.Column(db.String(100))
    tecladoMarca = db.Column(db.String(100))
    tecladoSerial = db.Column(db.String(100))
    mouseMarca = db.Column(db.String(100))
    mouseSerial = db.Column(db.String(100))
    nombreUsuario = db.Column(db.String(100))
    direccionMac = db.Column(db.String(100), primary_key=True)
    Observaciones = db.Column(db.String(500))
    VPN = db.Column(db.String(100))
    NombreRemoto = db.Column(db.String(100))
    Estado = db.Column(db.String(50))

class Mantenimientos(db.Model):
    __tablename__ = 'Mantenimientos'
    DireccionMac = db.Column(db.String(50), primary_key=True)
    Fecha = db.Column(db.String(20))
    Observaciones = db.Column(db.Text)
    Tecnico = db.Column(db.String(100))
    ResponsableEquipo = db.Column(db.String(100))

@app.route('/')
def index():
    try:
        # Verificar si hay registros en la tabla
        total_registros = Datospc.query.count()
        print(f"Total de registros en la tabla: {total_registros}")
        
        # Obtener todos los registros para ver sus estados
        todos_equipos = Datospc.query.all()
        print("Estados de todos los registros:")
        for equipo in todos_equipos:
            print(f"Placa: {equipo.placaSerial}, Estado: {equipo.Estado}")
        
        # Intentar la consulta filtrada

        equipos = Datospc.query.filter(func.trim(func.lower(Datospc.Estado)) == 'activo').all()
        print(f"Registros activos encontrados: {len(equipos)}")
        
        return render_template('index.html', equipos=equipos)
    except Exception as e:
        print(f"Error al consultar la base de datos: {str(e)}")
        return render_template('index.html', equipos=[])

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nuevo_equipo = Datospc(
            placaSerial=request.form['placaSerial'],
            responsable=request.form['responsable'],
            Ubicacion=request.form['Ubicacion'],
            nombreEquipo=request.form['nombreEquipo'],
            cpuFabricante=request.form['cpuFabricante'],
            cpuSerial=request.form['cpuSerial'],
            cpuPlaca=request.form['cpuPlaca'],
            procesadorNombre=request.form['procesadorNombre'],
            procesadorVelo=request.form['procesadorVelo'],
            procesadorSerial=request.form['procesadorSerial'],
            ram1Marca=request.form['ram1Marca'],
            ram1capacidad=request.form['ram1capacidad'],
            ram1Serial=request.form['ram1Serial'],
            ram2Marca=request.form['ram2Marca'],
            ram2Capacidad=request.form['ram2Capacidad'],
            ram2Serial=request.form['ram2Serial'],
            discoMarca=request.form['discoMarca'],
            discoCapacidad=request.form['discoCapacidad'],
            discoSerial=request.form['discoSerial'],
            unidadCD=request.form['unidadCD'],
            unidadCDSerial=request.form['unidadCDSerial'],
            monitorMarca=request.form['monitorMarca'],
            monitorModelo=request.form['monitorModelo'],
            monitorSerial=request.form['monitorSerial'],
            monitorPlaca=request.form['monitorPlaca'],
            tecladoMarca=request.form['tecladoMarca'],
            tecladoSerial=request.form['tecladoSerial'],
            mouseMarca=request.form['mouseMarca'],
            mouseSerial=request.form['mouseSerial'],
            nombreUsuario=request.form['nombreUsuario'],
            direccionMac=request.form['direccionMac'],
            Observaciones=request.form['Observaciones'],
            VPN=request.form['VPN'],
            NombreRemoto=request.form['NombreRemoto'],
            Estado='Activo'
        )
        db.session.add(nuevo_equipo)
        db.session.commit()
        flash('Equipo creado exitosamente')
        return redirect(url_for('index'))
    return render_template('crear.html')

@app.route('/editar/<direccionMac>', methods=['GET', 'POST'])
def editar(direccionMac):
    equipo = Datospc.query.get_or_404(direccionMac)
    direccionMac_anterior = equipo.direccionMac
    if request.method == 'POST':
        equipo.responsable = request.form['responsable']
        equipo.Ubicacion = request.form['Ubicacion']
        equipo.nombreEquipo = request.form['nombreEquipo']
        equipo.cpuFabricante = request.form['cpuFabricante']
        equipo.cpuSerial = request.form['cpuSerial']
        equipo.cpuPlaca = request.form['cpuPlaca']
        equipo.procesadorNombre = request.form['procesadorNombre']
        equipo.procesadorVelo = request.form['procesadorVelo']
        equipo.procesadorSerial = request.form['procesadorSerial']
        equipo.ram1Marca = request.form['ram1Marca']
        equipo.ram1capacidad = request.form['ram1capacidad']
        equipo.ram1Serial = request.form['ram1Serial']
        equipo.ram2Marca = request.form['ram2Marca']
        equipo.ram2Capacidad = request.form['ram2Capacidad']
        equipo.ram2Serial = request.form['ram2Serial']
        equipo.discoMarca = request.form['discoMarca']
        equipo.discoCapacidad = request.form['discoCapacidad']
        equipo.discoSerial = request.form['discoSerial']
        equipo.unidadCD = request.form['unidadCD']
        equipo.unidadCDSerial = request.form['unidadCDSerial']
        equipo.monitorMarca = request.form['monitorMarca']
        equipo.monitorModelo = request.form['monitorModelo']
        equipo.monitorSerial = request.form['monitorSerial']
        equipo.monitorPlaca = request.form['monitorPlaca']
        equipo.tecladoMarca = request.form['tecladoMarca']
        equipo.tecladoSerial = request.form['tecladoSerial']
        equipo.mouseMarca = request.form['mouseMarca']
        equipo.mouseSerial = request.form['mouseSerial']
        equipo.nombreUsuario = request.form['nombreUsuario']
        equipo.Observaciones = request.form['Observaciones']
        equipo.VPN = request.form['VPN']
        equipo.NombreRemoto = request.form['NombreRemoto']
        equipo.Sede = request.form['Sede']
        nueva_mac = request.form['direccionMac']
        if nueva_mac != direccionMac_anterior:
            # Actualizar la clave primaria y los mantenimientos
            mantenimientos = Mantenimientos.query.filter_by(DireccionMac=direccionMac_anterior).all()
            for mant in mantenimientos:
                mant.DireccionMac = nueva_mac
            equipo.direccionMac = nueva_mac
        db.session.commit()
        flash('Equipo actualizado exitosamente')
        return redirect(url_for('index'))
    return render_template('editar.html', equipo=equipo)

@app.route('/eliminar/<direccionMac>')
def eliminar(direccionMac):
    equipo = Datospc.query.get_or_404(direccionMac)
    equipo.Estado = 'Inactivo'
    db.session.commit()
    flash('Equipo marcado como inactivo')
    return redirect(url_for('index'))

@app.route('/generar_reporte/<direccionMac>')
def generar_reporte(direccionMac):
    equipo = Datospc.query.get_or_404(direccionMac)
    pdf = crear_hoja_vida_pdf(equipo)
    return send_file(
        BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'hoja_vida_{equipo.placaSerial}.pdf'
    )

@app.route('/mantenimientos', methods=['GET', 'POST'])
def mantenimientos():
    equipos = Datospc.query.all()
    if request.method == 'POST':
        nuevo_mant = Mantenimientos(
            DireccionMac=request.form['DireccionMac'],
            Fecha=request.form['Fecha'],
            Observaciones=request.form['Observaciones'],
            Tecnico=request.form['Tecnico'],
            ResponsableEquipo=request.form['ResponsableEquipo']
        )
        db.session.add(nuevo_mant)
        db.session.commit()
        flash('Mantenimiento registrado exitosamente')
        return redirect(url_for('mantenimientos'))
    mantenimientos = Mantenimientos.query.all()
    # Enriquecer mantenimientos con nombreEquipo y Ubicacion
    mantenimientos_enriquecidos = []
    for mant in mantenimientos:
        equipo = Datospc.query.filter_by(direccionMac=mant.DireccionMac).first()
        nombreEquipo = equipo.nombreEquipo if equipo else ''
        ubicacion = equipo.Ubicacion if equipo else ''
        mantenimientos_enriquecidos.append({
            'DireccionMac': mant.DireccionMac,
            'Fecha': mant.Fecha,
            'Observaciones': mant.Observaciones,
            'Tecnico': mant.Tecnico,
            'ResponsableEquipo': mant.ResponsableEquipo,
            'nombreEquipo': nombreEquipo,
            'Ubicacion': ubicacion
        })
    return render_template('mantenimientos.html', mantenimientos=mantenimientos_enriquecidos, equipos=equipos)

@app.route('/hoja_vida_html/<direccionMac>')
def hoja_vida_html(direccionMac):
    equipo = Datospc.query.get_or_404(direccionMac)
    mantenimientos = []
    if equipo.direccionMac:
        mantenimientos = Mantenimientos.query.filter_by(DireccionMac=equipo.direccionMac).all()
    return render_template('hoja_vida_equipo.html', equipo=equipo, mantenimientos=mantenimientos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 