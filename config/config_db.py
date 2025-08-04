from dotenv import load_dotenv
import os

load_dotenv()

# Carpeta local donde se guardarán los archivos adjuntos
RUTA_ARCHIVO = os.getenv("RUTA_ARCHIVO")

# Configuración db para servidor
DRIVER = os.getenv("DRIVER")
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
TRUSTSERVERCERTIFICATE = os.getenv("TRUSTSERVERCERTIFICATE")

# Configuración db para local
# DRIVER = os.getenv("DRIVER")
# SERVER = os.getenv("SERVER")
# DATABASE = os.getenv("DATABASE")
# TRUSTED_CONNECTION = os.getenv("TRUSTED_CONNECTION")
