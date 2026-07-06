import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3

def inicializar_base_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            nodo_id TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("\n[BASE DE DATOS] Archivo 'usuarios.db' creado e inicializado con exito.")

if __name__ == '__main__':
    inicializar_base_datos()
