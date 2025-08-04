import os
import sys
from outlook.outlook_client import OutlookClient
from outlook.utils import save_attachments_from_mail
from config.config_outlook import ATTACHMENT_DOWNLOAD_PATH
from procesamiento.utils import (
    leer_y_limpiar_archivo,
    obtener_archivo_del_dia,
    listar_archivos_validos,
    obtener_fecha_de_archivo
)
from procesamiento.db import conectar_sql_server
from procesamiento.procesamiento import procesar_fila

def descargar_archivo_desde_outlook():
    outlook = OutlookClient()
    emails = outlook.get_emails()

    if emails.Count == 0:
        print("❌ No hay correos en la carpeta.")
        return False

    emails.Sort("[ReceivedTime]", True)
    latest_email = emails.Item(1)

    try:
        save_attachments_from_mail(latest_email, ATTACHMENT_DOWNLOAD_PATH)
        print("📎 Archivo descargado correctamente desde Outlook.")
        return True
    except Exception as e:
        print(f"❌ Error descargando adjunto: {e}")
        return False

def procesar_archivo(ruta_archivo):
    fecha_archivo = obtener_fecha_de_archivo(ruta_archivo)
    print(f"📄 Procesando archivo: {os.path.basename(ruta_archivo)} (fecha_carga={fecha_archivo.date()})")

    df = leer_y_limpiar_archivo(ruta_archivo)
    print("🔌 Conectando a SQL Server...")
    conn = conectar_sql_server()
    cursor = conn.cursor()

    print(f"📝 Procesando {len(df)} registros...")
    for _, fila in df.iterrows():
        procesar_fila(cursor, fila, fecha_carga=fecha_archivo)

    conn.commit()
    conn.close()
    print("✅ Datos cargados correctamente en la base de datos.")

def main():
    modo = "masivo"  # Cambiar a "masivo" si se desea procesar todos los archivos de la carpeta

    if modo == "individual":
        if descargar_archivo_desde_outlook():
            archivo = obtener_archivo_del_dia(ATTACHMENT_DOWNLOAD_PATH)
            if archivo:
                procesar_archivo(archivo)
            else:
                print("⚠️ No se encontró el archivo esperado del día.")
        else:
            print("⛔ No se descargó ningún archivo. Proceso cancelado.")
    elif modo == "masivo":
        archivos = listar_archivos_validos(ATTACHMENT_DOWNLOAD_PATH)
        if not archivos:
            print("⚠️ No se encontraron archivos válidos en la carpeta.")
            return

        for archivo in archivos:
            procesar_archivo(archivo)
    else:
        print("❌ Modo inválido. Usa 'individual' o 'masivo'.")

if __name__ == "__main__":
    main()
