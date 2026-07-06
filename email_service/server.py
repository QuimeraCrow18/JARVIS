import os, sys, smtplib, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Email Service", version="2.0")

SMTP = os.getenv("SMTP_SERVER", "smtp.brevo.com")
SPORT = int(os.getenv("SMTP_PORT", "587"))
SUSER = os.getenv("SMTP_USER", "")
SPASS = os.getenv("SMTP_PASS", "")
FROM = os.getenv("FROM_EMAIL", "notificaciones@kexpler.com")
FNAME = os.getenv("FROM_NAME", "Kexpler Network")
LOGDIR = os.getenv("MAIL_LOG_DIR", "/app/data/mail_logs")
os.makedirs(LOGDIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOGDIR, "mail.log"), level=logging.INFO)
TPLDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

class MailPayload(BaseModel):
    to_email: str; subject: str; template_name: str = "welcome.html"; template_vars: dict = {}

def _render(tpl, vars):
    p = os.path.join(TPLDIR, tpl)
    if not os.path.exists(p): raise HTTPException(404, f"Template {tpl} no encontrado")
    with open(p, encoding="utf-8") as f: return Template(f.read()).safe_substitute(vars)

@app.post("/email/send")
async def send(p: MailPayload):
    if not SUSER or not SPASS:
        logging.info(f"[LOG] to={p.to_email}, subject={p.subject}")
        return {"status": "logged", "message": "SMTP no configurado, correo registrado en log"}
    try:
        html = _render(p.template_name, p.template_vars)
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{FNAME} <{FROM}>"
        msg["To"] = p.to_email; msg["Subject"] = p.subject
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP(SMTP, SPORT) as s:
            s.starttls(); s.login(SUSER, SPASS)
            s.sendmail(FROM, p.to_email, msg.as_string())
        logging.info(f"[ENVIADO] to={p.to_email}")
        return {"status": "sent"}
    except Exception as e:
        logging.error(f"[ERROR] {e}")
        raise HTTPException(500, str(e))

@app.get("/email/health")
async def health():
    return {"status": "ok", "service": "email_service", "smtp_configured": bool(SUSER and SPASS)}
