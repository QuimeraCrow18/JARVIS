import os, sqlite3, time, hashlib

DB = os.getenv("AUTH_DB_PATH", "/app/data/users/auth.db")

def _conn():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init():
    c = _conn()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT DEFAULT 'Pre-registrado',
            estado TEXT DEFAULT 'Pendiente',
            created_at REAL NOT NULL,
            approved_at REAL, approved_by TEXT
        );
        CREATE TABLE IF NOT EXISTS tokens (
            user_id INTEGER, token TEXT UNIQUE, expires REAL,
            FOREIGN KEY(user_id) REFERENCES usuarios(id)
        );
    """)
    c.commit(); c.close()

def _hash(p): return hashlib.sha256(p.encode()).hexdigest()

def register(email, username, password):
    c = _conn()
    try:
        c.execute("INSERT INTO usuarios (email, username, password_hash, created_at) VALUES (?,?,?,?)", (email, username, _hash(password), time.time()))
        c.commit()
        uid = c.lastrowid
        c.close()
        return {"ok": True, "user_id": uid}
    except sqlite3.IntegrityError:
        c.close()
        return {"ok": False, "error": "email_or_username_exists"}

def login(email, password):
    c = _conn()
    r = c.execute("SELECT * FROM usuarios WHERE email=? AND password_hash=?", (email, _hash(password))).fetchone()
    c.close()
    return dict(r) if r else None

def approve(uid, admin="admin"):
    c = _conn()
    c.execute("UPDATE usuarios SET rol='Usuario', estado='Activo', approved_at=?, approved_by=? WHERE id=? AND estado='Pendiente'", (time.time(), admin, uid))
    ok = c.rowcount > 0
    c.commit(); c.close()
    return ok

def reject(uid):
    c = _conn()
    c.execute("UPDATE usuarios SET estado='Rechazado' WHERE id=? AND estado='Pendiente'", (uid,))
    ok = c.rowcount > 0
    c.commit(); c.close()
    return ok

def pending():
    c = _conn()
    r = c.execute("SELECT id, email, username, created_at FROM usuarios WHERE estado='Pendiente' ORDER BY created_at DESC").fetchall()
    c.close()
    return [dict(x) for x in r]

def get(uid):
    c = _conn()
    r = c.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
    c.close()
    return dict(r) if r else None

def store_token(uid, token, expires=86400):
    c = _conn()
    c.execute("INSERT INTO tokens (user_id, token, expires) VALUES (?,?,?)", (uid, token, time.time() + expires))
    c.commit(); c.close()

def verify_token(token):
    c = _conn()
    r = c.execute("SELECT user_id FROM tokens WHERE token=? AND expires>?", (token, time.time())).fetchone()
    c.close()
    return r[0] if r else None
