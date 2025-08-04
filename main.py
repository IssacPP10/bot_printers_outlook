import os
from datetime import datetime
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
from telegram.telegram_bot import enviar_mensaje, formato_log  # Ajusta la ruta si es necesario

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

def procesar_archivo(ruta_archivo, enviar_log_telegram=True):
    nombre_archivo = os.path.basename(ruta_archivo)
    fecha_archivo = obtener_fecha_de_archivo(ruta_archivo)

    if enviar_log_telegram:
        enviar_mensaje(formato_log(f"📄 Procesando archivo: <code>{nombre_archivo}</code> (fecha={fecha_archivo.date()})"))

    df = leer_y_limpiar_archivo(ruta_archivo)
    conn = conectar_sql_server()
    cursor = conn.cursor()

    if enviar_log_telegram:
        enviar_mensaje(formato_log(f"🔌 Conectando a SQL Server...\n📝 Registros: <b>{len(df)}</b>"))

    for _, fila in df.iterrows():
        procesar_fila(cursor, fila, fecha_carga=fecha_archivo)

    conn.commit()
    conn.close()

    if enviar_log_telegram:
        enviar_mensaje(formato_log(f"✅ <b>{nombre_archivo}</b> cargado correctamente en la base de datos."))

def main():
    modo = "masivo"  # Cambiar a "individual" si se desea solo 1 archivo
    inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    enviar_mensaje(formato_log(f"🚀 Inicio del proceso\n🕒 Fecha y hora: <b>{inicio}</b>\n⚙️ Modo: <b>{modo}</b>"))

    try:
        if modo == "individual":
            if descargar_archivo_desde_outlook():
                archivo = obtener_archivo_del_dia(ATTACHMENT_DOWNLOAD_PATH)
                if archivo:
                    enviar_mensaje(formato_log(f"📎 Archivo detectado: <code>{os.path.basename(archivo)}</code>"))
                    procesar_archivo(archivo)
                else:
                    enviar_mensaje(formato_log("⚠️ No se encontró el archivo esperado del día."))
            else:
                enviar_mensaje(formato_log("⛔ No se descargó ningún archivo. Proceso cancelado."))
        
        elif modo == "masivo":
            archivos = listar_archivos_validos(ATTACHMENT_DOWNLOAD_PATH)
            total = len(archivos)

            if total == 0:
                enviar_mensaje(formato_log("⚠️ No se encontraron archivos válidos en la carpeta."))
                return

            # Mostrar hasta 5 archivos como vista previa
            archivos_mostrados = archivos[:5]
            lista_resumen = "\n".join([f"• <code>{os.path.basename(a)}</code>" for a in archivos_mostrados])
            resumen = f"📦 Archivos detectados: <b>{total}</b>\n{lista_resumen}"

            if total > 5:
                resumen += f"\n... y <b>{total - 5}</b> más."

            enviar_mensaje(formato_log(resumen))

            # ⏳ Indicar que empieza el procesamiento
            enviar_mensaje(formato_log("⏳ Procesando archivos, esto puede tardar unos minutos. Por favor espera..."))

            for archivo in archivos:
                try:
                    procesar_archivo(archivo, enviar_log_telegram=False)  # Evita spam en masivo
                except Exception as e:
                    enviar_mensaje(formato_log(f"❌ Error procesando <code>{os.path.basename(archivo)}</code>:\n<code>{str(e)}</code>"))

            enviar_mensaje(formato_log("✅ <b>Proceso masivo finalizado correctamente.</b>"))

        else:
            enviar_mensaje(formato_log("❌ Modo inválido. Usa 'individual' o 'masivo'."))
            return

    except Exception as e:
        enviar_mensaje(formato_log(f"❌ <b>Error crítico durante la ejecución:</b>\n<code>{str(e)}</code>"))

if __name__ == "__main__":
    main()
