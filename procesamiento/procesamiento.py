from datetime import datetime
from .db import obtener_id

def procesar_fila(cursor, fila, fecha_carga=None):
    id_cedis = obtener_id(cursor, 'cedis', 'nombre', fila['cedis'], campo_id='id_cedis')

    cursor.execute("""
        SELECT id_ubicacion FROM Ubicaciones 
        WHERE ubicacion = ?
    """, fila['ubicacion'])
    depto = cursor.fetchone()
    if depto:
        id_depto = depto[0]
    else:
        cursor.execute("""
            INSERT INTO Ubicaciones (ubicacion) 
            OUTPUT INSERTED.id_ubicacion 
            VALUES (?)
        """, fila['ubicacion'])
        id_depto = cursor.fetchone()[0]

    cursor.execute("""
        SELECT id_impresora FROM Impresoras 
        WHERE numero_serie = ?
    """, fila['numero_serie'])
    impresora = cursor.fetchone()
    if impresora:
        id_impresora = impresora[0]
    else:
        cursor.execute("""
            INSERT INTO Impresoras (modelo, direccion_ip, numero_serie, mac_address)
            OUTPUT INSERTED.id_impresora 
            VALUES (?, ?, ?, ?)
        """, fila['modelo'], fila['direccion_ip'], fila['numero_serie'], fila['mac_address'])
        id_impresora = cursor.fetchone()[0]

    cursor.execute("""
        SELECT 1 FROM Impresora_Ubicacion 
        WHERE id_impresora = ? AND id_ubicacion = ? AND id_cedis = ?
    """, id_impresora, id_depto, id_cedis)
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO Impresora_Ubicacion (id_impresora, id_ubicacion, id_cedis)
            VALUES (?, ?, ?)
        """, id_impresora, id_depto, id_cedis)

    # Usar la fecha de carga si se proporcionó, si no usar datetime.now()
    fecha_final = fecha_carga if fecha_carga else datetime.now()

    cursor.execute("""
        INSERT INTO Lectura_Impresoras (
            id_impresora, total_bn, total_color,
            impresion_total_bn, impresion_total_color,
            copia_total_bn, copia_total_color, copia_total, 
            impresion_total, total_paginas, fecha_carga)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, id_impresora, 
         fila['total_bn'], fila['total_color'],
         fila['impresion_total_bn'], fila['impresion_total_color'],
         fila['copia_total_bn'], fila['copia_total_color'],
         fila['copia_total'], fila['impresion_total'], fila['total_paginas'],
         fecha_final)
