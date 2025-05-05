from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import os

# Definir colores personalizados
verde_oscuro = colors.HexColor('#2E7D32')  # Verde oscuro
verde_claro = colors.HexColor('#C8E6C9')   # Verde muy claro
verde_medio = colors.HexColor('#81C784')   # Verde medio
blanco = colors.white
gris_claro = colors.HexColor('#F5F5F5')    # Gris muy claro

def crear_hoja_vida_pdf(equipo):
    """
    Crea un reporte de hoja de vida en PDF para un equipo de cómputo.
    
    Args:
        equipo: Objeto Datospc con la información del equipo
        
    Returns:
        BytesIO: Objeto BytesIO con el PDF generado
    """
    # Crear un buffer para el PDF
    buffer = BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # Centrado
        spaceAfter=10,
        textColor=verde_oscuro,
        fontName='Helvetica-Bold'
    )
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=blanco,
        backColor=verde_oscuro,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        fontName='Helvetica'
    )
    
    # Contenido del PDF
    elements = []
    
    # Logo y Título
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=1.5*inch, height=1.5*inch)
        elements.append(img)
    
    elements.append(Paragraph("HOSPITAL DIVINO SALVADOR DE SOPÓ", title_style))
    elements.append(Paragraph("HOJA DE VIDA DE EQUIPO DE CÓMPUTO", title_style))
    elements.append(Spacer(1, 15))
    
    # Crear una tabla para organizar la información en dos columnas
    # Primera columna: Información Básica y CPU
    col1_data = []
    
    # Información Básica
    col1_data.append(["INFORMACIÓN BÁSICA", ""])
    col1_data.extend([
        ["Placa Serial", equipo.placaSerial],
        ["Responsable", equipo.responsable],
        ["Ubicación", equipo.Ubicacion],
        ["Sede", equipo.Sede],
        ["Nombre Usuario", equipo.nombreUsuario],
        ["Dirección MAC", equipo.direccionMac],
        ["VPN", equipo.VPN]
    ])
    
    # CPU y Procesador
    col1_data.append(["", ""])
    col1_data.append(["CPU Y PROCESADOR", ""])
    col1_data.extend([
        ["Fabricante CPU", equipo.cpuFabricante],
        ["Serial CPU", equipo.cpuSerial],
        ["Placa CPU", equipo.cpuPlaca],
        ["Nombre Procesador", equipo.procesadorNombre],
        ["Velocidad Procesador", equipo.procesadorVelo],
        ["Serial Procesador", equipo.procesadorSerial]
    ])
    
    # Segunda columna: RAM, Almacenamiento y Periféricos
    col2_data = []
    
    # Memoria RAM
    col2_data.append(["MEMORIA RAM", ""])
    col2_data.extend([
        ["Marca RAM 1", equipo.ram1Marca],
        ["Capacidad RAM 1", equipo.ram1capacidad],
        ["Serial RAM 1", equipo.ram1Serial],
        ["Marca RAM 2", equipo.ram2Marca],
        ["Capacidad RAM 2", equipo.ram2Capacidad],
        ["Serial RAM 2", equipo.ram2Serial]
    ])
    
    # Almacenamiento
    col2_data.append(["", ""])
    col2_data.append(["ALMACENAMIENTO", ""])
    col2_data.extend([
        ["Marca Disco", equipo.discoMarca],
        ["Capacidad Disco", equipo.discoCapacidad],
        ["Serial Disco", equipo.discoSerial],
        ["Unidad CD", equipo.unidadCD],
        ["Serial Unidad CD", equipo.unidadCDSerial]
    ])
    
    # Periféricos
    col2_data.append(["", ""])
    col2_data.append(["PERIFÉRICOS", ""])
    col2_data.extend([
        ["Marca Monitor", equipo.monitorMarca],
        ["Modelo Monitor", equipo.monitorModelo],
        ["Serial Monitor", equipo.monitorSerial],
        ["Placa Monitor", equipo.monitorPlaca],
        ["Marca Teclado", equipo.tecladoMarca],
        ["Serial Teclado", equipo.tecladoSerial],
        ["Marca Mouse", equipo.mouseMarca],
        ["Serial Mouse", equipo.mouseSerial]
    ])
    
    # Crear las tablas para cada columna
    col1_table = Table(col1_data, colWidths=[2*inch, 3*inch])
    col2_table = Table(col2_data, colWidths=[2*inch, 3*inch])
    
    # Estilo común para las tablas
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), gris_claro),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (0, -1), verde_claro),
        ('TEXTCOLOR', (0, 0), (0, -1), verde_oscuro),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, verde_medio),
        ('SPAN', (0, 0), (1, 0)),  # Para los encabezados de sección
        ('SPAN', (0, 7), (1, 7)),  # Para los encabezados de sección
        ('SPAN', (0, 0), (1, 0)),  # Para los encabezados de sección en col2
        ('SPAN', (0, 7), (1, 7)),  # Para los encabezados de sección en col2
        ('SPAN', (0, 14), (1, 14)),  # Para los encabezados de sección en col2
        ('BACKGROUND', (0, 0), (1, 0), verde_medio),  # Encabezados de sección
        ('BACKGROUND', (0, 7), (1, 7), verde_medio),  # Encabezados de sección
        ('BACKGROUND', (0, 0), (1, 0), verde_medio),  # Encabezados de sección en col2
        ('BACKGROUND', (0, 7), (1, 7), verde_medio),  # Encabezados de sección en col2
        ('BACKGROUND', (0, 14), (1, 14), verde_medio),  # Encabezados de sección en col2
        ('TEXTCOLOR', (0, 0), (1, 0), blanco),  # Texto de encabezados
        ('TEXTCOLOR', (0, 7), (1, 7), blanco),  # Texto de encabezados
        ('TEXTCOLOR', (0, 0), (1, 0), blanco),  # Texto de encabezados en col2
        ('TEXTCOLOR', (0, 7), (1, 7), blanco),  # Texto de encabezados en col2
        ('TEXTCOLOR', (0, 14), (1, 14), blanco)  # Texto de encabezados en col2
    ])
    
    col1_table.setStyle(table_style)
    col2_table.setStyle(table_style)
    
    # Crear una tabla contenedora para las dos columnas
    container_data = [[col1_table, col2_table]]
    container_table = Table(container_data, colWidths=[5*inch, 5*inch])
    container_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 10)
    ]))
    
    elements.append(container_table)
    elements.append(Spacer(1, 15))
    
    # Observaciones
    obs_style = ParagraphStyle(
        'CustomObs',
        parent=styles['Normal'],
        fontSize=10,
        textColor=verde_oscuro,
        fontName='Helvetica-Bold',
        alignment=1
    )
    elements.append(Paragraph("OBSERVACIONES", obs_style))
    elements.append(Paragraph(equipo.Observaciones or "Sin observaciones", normal_style))
    
    # Generar el PDF
    doc.build(elements)
    
    # Obtener el PDF del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf 