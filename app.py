from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from reporte_pdf import crear_hoja_vida_pdf
from sqlalchemy import func
from io import BytesIO
import google.generativeai as genai
import xml.etree.ElementTree as ET
import json

# Configuración de Gemini
genai.configure(api_key='AIzaSyAZklbUnZmdsxROcfETW0VZY0Kjy9QqB5U')
model = genai.GenerativeModel('gemini-1.5-flash')

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
    FirmaResponsable = db.Column(db.String(500))  # Campo para almacenar la firma

@app.route('/')
def index():
    try:
        # Obtener el término de búsqueda de la URL
        busqueda = request.args.get('busqueda', '').strip()
        
        # Base query para equipos activos
        query = Datospc.query.filter(func.trim(func.lower(Datospc.Estado)) == 'activo')
        
        # Si hay término de búsqueda, filtrar por ubicación
        if busqueda:
            query = query.filter(Datospc.Ubicacion.ilike(f'%{busqueda}%'))
        
        # Ejecutar la consulta
        equipos = query.all()
        print(f"Registros encontrados: {len(equipos)}")
        
        return render_template('index.html', equipos=equipos, busqueda=busqueda)
    except Exception as e:
        print(f"Error al consultar la base de datos: {str(e)}")
        return render_template('index.html', equipos=[], busqueda='')

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        # Verificar si la dirección MAC ya existe
        mac_existente = Datospc.query.filter_by(direccionMac=request.form['direccionMac']).first()
        if mac_existente:
            flash('Error: Ya existe un equipo registrado con esta dirección MAC', 'error')
            return redirect(url_for('crear'))

        nuevo_equipo = Datospc(
            placaSerial=request.form.get('placaSerial', ''),
            responsable=request.form.get('responsable', ''),
            Ubicacion=request.form.get('Ubicacion', ''),
            Sede=request.form.get('Sede', ''),
            nombreEquipo=request.form.get('nombreEquipo', ''),
            cpuFabricante=request.form.get('cpuFabricante', ''),
            cpuSerial=request.form.get('cpuSerial', ''),
            cpuPlaca=request.form.get('cpuPlaca', ''),
            procesadorNombre=request.form.get('procesadorNombre', ''),
            procesadorVelo=request.form.get('procesadorVelo', ''),
            procesadorSerial=request.form.get('procesadorSerial', ''),
            ram1Marca=request.form.get('ram1Marca', ''),
            ram1capacidad=request.form.get('ram1capacidad', ''),
            ram1Serial=request.form.get('ram1Serial', ''),
            ram2Marca=request.form.get('ram2Marca', ''),
            ram2Capacidad=request.form.get('ram2Capacidad', ''),
            ram2Serial=request.form.get('ram2Serial', ''),
            discoMarca=request.form.get('discoMarca', ''),
            discoCapacidad=request.form.get('discoCapacidad', ''),
            discoSerial=request.form.get('discoSerial', ''),
            unidadCD=request.form.get('unidadCD', ''),
            unidadCDSerial=request.form.get('unidadCDSerial', ''),
            monitorMarca=request.form.get('monitorMarca', ''),
            monitorModelo=request.form.get('monitorModelo', ''),
            monitorSerial=request.form.get('monitorSerial', ''),
            monitorPlaca=request.form.get('monitorPlaca', ''),
            tecladoMarca=request.form.get('tecladoMarca', ''),
            tecladoSerial=request.form.get('tecladoSerial', ''),
            mouseMarca=request.form.get('mouseMarca', ''),
            mouseSerial=request.form.get('mouseSerial', ''),
            nombreUsuario=request.form.get('nombreUsuario', ''),
            direccionMac=request.form['direccionMac'],  # Este campo es obligatorio
            Observaciones=request.form.get('Observaciones', ''),
            VPN=request.form.get('VPN', ''),
            NombreRemoto=request.form.get('NombreRemoto', ''),
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
        mantenimientos = Mantenimientos.query.filter_by(DireccionMac=equipo.direccionMac).order_by(Mantenimientos.Fecha.desc()).all()
    return render_template('hoja_vida_equipo.html', equipo=equipo, mantenimientos=mantenimientos)

@app.route('/procesar_xml', methods=['POST'])
def procesar_xml():
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    if not file.filename.lower().endswith('.xml'):
        return jsonify({'error': 'El archivo debe ser XML'}), 400
    
    try:
        # Leer el contenido del XML
        xml_content = file.read().decode('utf-8')
        print("Contenido XML leído correctamente")
        
        # Preparar el prompt para Gemini
        prompt = f"""
        Analiza el siguiente texto XML y extrae la siguiente información. Si no encuentras algún dato, responde "No encontrada".
        IMPORTANTE: Debes responder SOLO con un objeto JSON válido, sin texto adicional antes o después, sin marcadores de código.
        
        Texto XML a analizar:
        {xml_content}
        
        Necesito los siguientes datos en formato JSON:
        {{
            "placaSerial": "valor o No encontrada",
            "cpuFabricante": "valor o No encontrada",
            "cpuSerial": "valor o No encontrada",
            "procesadorNombre": "valor o No encontrada",
            "procesadorVelo": "valor o No encontrada",
            "procesadorSerial": "valor o No encontrada",
            "nombreEquipo": "valor o No encontrada",
            "ram1Marca": "valor o No encontrada",
            "ram1capacidad": "valor o No encontrada",
            "ram1Serial": "valor o No encontrada",
            "ram2Marca": "valor o No encontrada",
            "ram2Capacidad": "valor o No encontrada",
            "ram2Serial": "valor o No encontrada",
            "discoCapacidad": "valor o No encontrada",
            "discoSerial": "valor o No encontrada",
            "nombreUsuario": "valor o No encontrada",
            "direccionMac": "valor o No encontrada",
            "unidadCD": "valor o No encontrada",
            "unidadCDSerial": "valor o No encontrada",
            "monitorMarca": "valor o No encontrada",
            "monitorModelo": "valor o No encontrada",
            "monitorSerial": "valor o No encontrada",
            "tecladoMarca": "valor o No encontrada",
            "tecladoSerial": "valor o No encontrada",
            "mouseMarca": "valor o No encontrada",
            "mouseSerial": "valor o No encontrada"
        }}
        """
        
        print("Enviando prompt a Gemini...")
        # Obtener respuesta de Gemini
        response = model.generate_content(prompt)
        print("Respuesta recibida de Gemini:", response.text)
        
        try:
            # Limpiar la respuesta de marcadores de código
            json_text = response.text
            json_text = json_text.replace('```json', '').replace('```', '').strip()
            print("JSON limpio:", json_text)
            
            datos = json.loads(json_text)
            print("JSON parseado correctamente")
            return jsonify(datos)
        except json.JSONDecodeError as e:
            print("Error al parsear JSON:", str(e))
            print("Texto recibido:", response.text)
            return jsonify({'error': 'Error al procesar la respuesta de Gemini. Por favor, intente nuevamente.'}), 500
        
    except Exception as e:
        print("Error general:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/firmas_pendientes')
def firmas_pendientes():
    try:
        # Obtener mantenimientos sin firma
        mantenimientos_pendientes = db.session.query(Mantenimientos, Datospc).\
            join(Datospc, Mantenimientos.DireccionMac == Datospc.direccionMac).\
            filter(Mantenimientos.FirmaResponsable.is_(None)).all()
        
        return render_template('firmas_pendientes.html', mantenimientos=mantenimientos_pendientes)
    except Exception as e:
        print(f"Error al consultar mantenimientos pendientes: {str(e)}")
        return render_template('firmas_pendientes.html', mantenimientos=[])

@app.route('/firmar_mantenimiento/<direccionMac>', methods=['GET', 'POST'])
def firmar_mantenimiento(direccionMac):
    if request.method == 'POST':
        try:
            mantenimiento = Mantenimientos.query.get_or_404(direccionMac)
            mantenimiento.FirmaResponsable = request.form.get('firma')
            db.session.commit()
            flash('Firma registrada exitosamente', 'success')
            return redirect(url_for('firmas_pendientes'))
        except Exception as e:
            flash(f'Error al registrar la firma: {str(e)}', 'error')
            return redirect(url_for('firmas_pendientes'))
    
    mantenimiento = Mantenimientos.query.get_or_404(direccionMac)
    equipo = Datospc.query.get_or_404(direccionMac)
    return render_template('firmar.html', mantenimiento=mantenimiento, equipo=equipo)

if __name__ == '__main__':
    app.run(port=5001)
    with app.app_context():
        db.create_all()
    app.run(debug=True)