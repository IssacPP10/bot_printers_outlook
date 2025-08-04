import os
import datetime
import re

def sanitize_filename(filename):
    # Elimina caracteres no válidos en Windows
    return re.sub(r'[<>:"/\\|?*]', "_", filename)

def save_attachments_from_mail(mail_item, download_path):
    if not mail_item.Attachments.Count:
        return

    os.makedirs(download_path, exist_ok=True)

    for i in range(1, mail_item.Attachments.Count + 1):
        try:
            attachment = mail_item.Attachments.Item(i)
            original_ext = os.path.splitext(attachment.FileName)[1]

            # Solo fecha actual
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            new_filename = f"Reporte_Impresoras_{today}{original_ext}"
            new_filename = sanitize_filename(new_filename)
            file_path = os.path.join(download_path, new_filename)

            # Guardar el archivo (reemplaza si ya existe)
            attachment.SaveAsFile(file_path)
            print(f"✅ Guardado (reemplazado si existía): {file_path}")

        except Exception as e:
            print(f"❌ Error guardando adjunto: {e}")
