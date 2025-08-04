import os
import pandas as pd
from datetime import datetime

def obtener_archivo_del_dia(carpeta: str) -> str:
    hoy = datetime.today().strftime('%Y-%m-%d')
    nombre_esperado = f"Reporte_Impresoras_{hoy}.csv"
    ruta_archivo = os.path.join(carpeta, nombre_esperado)
    return ruta_archivo if os.path.exists(ruta_archivo) else None

def listar_archivos_validos(carpeta: str) -> list:
    archivos = []
    for archivo in os.listdir(carpeta):
        if archivo.startswith("Reporte_Impresoras_") and archivo.endswith(".csv"):
            archivos.append(os.path.join(carpeta, archivo))
    return sorted(archivos)

def obtener_fecha_de_archivo(nombre_archivo: str) -> datetime:
    base = os.path.basename(nombre_archivo)
    try:
        fecha_str = base.replace("Reporte_Impresoras_", "").replace(".csv", "")
        return datetime.strptime(fecha_str, "%Y-%m-%d")
    except Exception:
        return datetime.today()

def leer_y_limpiar_archivo(ruta):
    df = pd.read_csv(ruta)
    # print("Columnas antes de renombrar:", df.columns.tolist())
    df.rename(columns={
        'Impresora': 'cedis',
        'Modelo': 'modelo',
        'Direccion-IP': 'direccion_ip',
        'Número de serie': 'numero_serie',
        'MAC-address': 'mac_address',
        'Departamento': 'nombre_departamento',
        'Ubicación': 'ubicacion',
        'Total, B/N': 'total_bn',
        'Total, color': 'total_color',
        'impresion_total_bn': 'impresion_total_bn',
        'impresion_total_color': 'impresion_total_color',
        'copia_total_bn': 'copia_total_bn',
        'copia_total_color': 'copia_total_color',
        'Copia total': 'copia_total',
        'Impresion total': 'impresion_total',
        'Total pages': 'total_paginas'
    }, inplace=True)

    # Rellenar valores nulos
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('NA')
        else:
            df[col] = df[col].fillna(0)

    # Si no viene 'total_paginas', crearlo manualmente
    if 'total_paginas' not in df.columns:
        df['total_paginas'] = (
            df.get('copia_total', 0) + df.get('impresion_total', 0)
        )


    return df
