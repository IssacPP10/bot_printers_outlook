from dotenv import load_dotenv
import os

load_dotenv()

# Nombre de la cuenta de Outlook (tal como aparece en Outlook)
OUTLOOK_ACCOUNT_NAME = os.getenv("OUTLOOK_ACCOUNT_NAME")

# Nombre exacto de la carpeta donde llegan los correos con adjuntos
TARGET_FOLDER_NAME = os.getenv("TARGET_FOLDER_NAME")

# Carpeta local donde se guardarán los archivos adjuntos
ATTACHMENT_DOWNLOAD_PATH = os.getenv("RUTA_ARCHIVO")
