import pyodbc
from config.config_db import DRIVER, SERVER, DATABASE, USER, PASSWORD, TRUSTSERVERCERTIFICATE

# Configuración db para servidor
def conectar_sql_server():
    return pyodbc.connect(
        f'DRIVER={DRIVER};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USER};'
        f'PWD={PASSWORD};'
        f'TrustServerCertificate={TRUSTSERVERCERTIFICATE};'
        f'Encrypt=yes;'
    )

# Configuración db para local
# def conectar_sql_server():
#     return pyodbc.connect(
#         f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection={TRUSTED_CONNECTION};Encrypt=no"
#     )


def obtener_id(cursor, tabla, campo_busqueda, valor, campo_id='id'):
    cursor.execute(f"SELECT {campo_id} FROM {tabla} WHERE {campo_busqueda} = ?", valor)
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(f"INSERT INTO {tabla} ({campo_busqueda}) OUTPUT INSERTED.{campo_id} VALUES (?)", valor)
    return cursor.fetchone()[0]
