import sys, os, sqlite3, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from security.oceanic_shield import OceanicShield

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kexpler_cloud.db")
clave = "CLAVE_MAESTRA_INTEGRACION"

def limpiar():
    if os.path.exists(DB):
        os.remove(DB)

def crear_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre_cifrado TEXT, email_cifrado TEXT)")
    conn.commit()
    conn.close()

def registrar_usuario_kexpler(uid, nombre, email):
    o = OceanicShield(clave)
    nc = o.encriptar(nombre)
    ec = o.encriptar(email)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (id, nombre_cifrado, email_cifrado) VALUES (?, ?, ?)", (uid, nc, ec))
    conn.commit()
    conn.close()
    return {"nc": nc[:20]+"...", "ec": ec[:20]+"..."}

def leer_y_validar_josamick(uid, esperado_nombre, esperado_email):
    o = OceanicShield(clave)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT nombre_cifrado, email_cifrado FROM usuarios WHERE id = ?", (uid,))
    fila = cur.fetchone()
    conn.close()
    if not fila:
        return False, "No se encontro el usuario"
    nombre = o.desencriptar(fila[0])
    email = o.desencriptar(fila[1])
    ok_nom = nombre == esperado_nombre
    ok_email = email == esperado_email
    return (ok_nom and ok_email), {"nombre": nombre, "email": email, "coincide_nombre": ok_nom, "coincide_email": ok_email}

if __name__ == "__main__":
    print("=" * 50)
    print("FASE 1: PRUEBA DE INTEGRACION CRIPTOGRAFICA")
    print("=" * 50)
    limpiar()
    crear_db()
    print("\n[KEXPLER] Registrando usuario 1...")
    res = registrar_usuario_kexpler(1, "Alexis Josamick", "alexis@josamick.ai")
    print(f"  Nombre cifrado: {res['nc']}")
    print(f"  Email cifrado:  {res['ec']}")
    print("\n[JOSAMICK] Leyendo y desencriptando desde la misma DB...")
    ok, detalle = leer_y_validar_josamick(1, "Alexis Josamick", "alexis@josamick.ai")
    if ok:
        print(f"  Nombre desencriptado: {detalle['nombre']}")
        print(f"  Email desencriptado:  {detalle['email']}")
        print("\n>>> PUENTE CRIPTOGRAFICO BIDIRECCIONAL: OK")
    else:
        print(f"\n>>> FALLO: {detalle}")
    print("=" * 50)
