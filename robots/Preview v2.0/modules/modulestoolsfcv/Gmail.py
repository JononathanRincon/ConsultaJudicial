"""
gmail_notificador.py
====================
Lee los correos NO LEÍDOS de Gmail usando IMAP y envía
un resumen de notificación a otra cuenta de correo vía SMTP.

Requisitos:
    pip install python-dotenv

Configuración previa en Gmail:
    1. Activar verificación en 2 pasos en tu cuenta Google.
    2. Ir a: https://myaccount.google.com/apppasswords
    3. Crear una App Password (nombre: "Python Notificador").
    4. Copiar la clave generada (16 caracteres) en GMAIL_APP_PASSWORD.
    5. Asegurarte de que IMAP esté activado en:
       Gmail → Configuración → Ver todos los ajustes → Reenvío e IMAP → Habilitar IMAP
"""

import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN — edita estos valores
# ─────────────────────────────────────────────

GMAIL_USER = "jonathandevrpa@gmail.com"  # Tu cuenta Gmail (origen)
GMAIL_APP_PASSWORD = "kigo wmub ndpk qwmj"  # App Password de Google (16 chars)

DESTINO_EMAIL = "jonathanandres080@gmail.com"  # Correo donde recibes la notificación
DESTINO_NOMBRE = "Jonathan Rincon"  # Nombre del destinatario (opcional)

MAX_CORREOS = 30  # Máximo de no leídos a procesar
CARPETA_IMAP = "INBOX"  # Carpeta a revisar

# ─────────────────────────────────────────────
# FUNCIÓN: Decodificar encabezados del correo
# ─────────────────────────────────────────────


def decodificar(valor):
    """Decodifica encabezados que pueden venir en base64 o utf-8."""
    if valor is None:
        return "(sin valor)"
    partes = decode_header(valor)
    resultado = []
    for contenido, codificacion in partes:
        if isinstance(contenido, bytes):
            try:
                resultado.append(
                    contenido.decode(codificacion or "utf-8", errors="replace")
                )
            except Exception:
                resultado.append(contenido.decode("latin-1", errors="replace"))
        else:
            resultado.append(contenido)
    return "".join(resultado)


# ─────────────────────────────────────────────
# FUNCIÓN: Extraer texto plano del mensaje
# ─────────────────────────────────────────────


def obtener_cuerpo(msg):
    """Extrae el cuerpo en texto plano de un mensaje email."""
    cuerpo = ""
    if msg.is_multipart():
        for parte in msg.walk():
            tipo = parte.get_content_type()
            disposicion = str(parte.get("Content-Disposition", ""))
            if tipo == "text/plain" and "attachment" not in disposicion:
                charset = parte.get_content_charset() or "utf-8"
                try:
                    cuerpo = parte.get_payload(decode=True).decode(
                        charset, errors="replace"
                    )
                except Exception:
                    cuerpo = "(no se pudo leer el cuerpo)"
                break
    else:
        charset = msg.get_content_charset() or "utf-8"
        try:
            cuerpo = msg.get_payload(decode=True).decode(charset, errors="replace")
        except Exception:
            cuerpo = "(no se pudo leer el cuerpo)"
    return cuerpo.strip()


# ─────────────────────────────────────────────
# FUNCIÓN: Leer correos no leídos desde Gmail
# ─────────────────────────────────────────────


def leer_no_leidos():
    """Conecta a Gmail por IMAP y retorna lista de correos no leídos."""
    print(f"[INFO] Conectando a Gmail IMAP como {GMAIL_USER}...")

    correos = []

    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        imap.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        imap.select(CARPETA_IMAP)

        # Buscar solo los no leídos
        estado, ids = imap.search(None, "UNSEEN")

        if estado != "OK" or not ids[0]:
            print("[INFO] No hay correos no leídos.")
            imap.logout()
            return correos

        lista_ids = ids[0].split()
        print(f"[INFO] Encontrados {len(lista_ids)} correos no leídos.")

        # Tomar solo los últimos MAX_CORREOS (más recientes)
        lista_ids = lista_ids[-MAX_CORREOS:]

        for uid in reversed(lista_ids):  # Del más reciente al más antiguo
            _, datos = imap.fetch(uid, "(RFC822)")
            msg_raw = datos[0][1]
            msg = email.message_from_bytes(msg_raw)

            asunto = decodificar(msg.get("Subject", "(sin asunto)"))
            remit = decodificar(msg.get("From", "(desconocido)"))
            fecha = msg.get("Date", "(sin fecha)")
            cuerpo = obtener_cuerpo(msg)

            # Limitar preview del cuerpo a 300 caracteres
            preview = cuerpo[:300] + ("..." if len(cuerpo) > 300 else "")

            correos.append(
                {
                    "asunto": asunto,
                    "de": remit,
                    "fecha": fecha,
                    "preview": preview,
                }
            )

        imap.logout()

    except imaplib.IMAP4.error as e:
        print(f"[ERROR] Fallo de autenticación IMAP: {e}")
        print(
            "  → Verifica que el App Password sea correcto y que IMAP esté habilitado."
        )
    except Exception as e:
        print(f"[ERROR] Error al leer correos: {e}")

    return correos


# ─────────────────────────────────────────────
# FUNCIÓN: Construir cuerpo HTML del resumen
# ─────────────────────────────────────────────


def construir_html(correos):
    """Genera el HTML del correo de notificación."""
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    total = len(correos)

    filas_html = ""
    for i, c in enumerate(correos, 1):
        filas_html += f"""
        <tr style="background:{"#f9f9f9" if i % 2 == 0 else "#ffffff"};">
            <td style="padding:10px;border-bottom:1px solid #eee;font-weight:bold;color:#333;">{i}</td>
            <td style="padding:10px;border-bottom:1px solid #eee;">
                <strong style="color:#1a73e8;">{c["asunto"]}</strong><br>
                <span style="color:#888;font-size:12px;">De: {c["de"]}</span><br>
                <span style="color:#aaa;font-size:11px;">{c["fecha"]}</span>
            </td>
            <td style="padding:10px;border-bottom:1px solid #eee;color:#555;font-size:13px;">
                {c["preview"]}
            </td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family:Arial,sans-serif;background:#f0f4f8;padding:20px;">
        <div style="max-width:800px;margin:auto;background:#fff;border-radius:10px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;">

            <!-- Encabezado -->
            <div style="background:#1a73e8;padding:24px 30px;">
                <h1 style="color:#fff;margin:0;font-size:22px;">📬 Resumen de Correos No Leídos</h1>
                <p style="color:#c8dcff;margin:6px 0 0;font-size:14px;">
                    Generado el {ahora} · {total} mensaje{
        "s" if total != 1 else ""
    } no leído{"s" if total != 1 else ""}
                </p>
            </div>

            <!-- Tabla de correos -->
            <div style="padding:20px;">
                {
        '<p style="color:#888;text-align:center;padding:40px 0;">✅ No tienes correos no leídos.</p>'
        if total == 0
        else f'''
                <table style="width:100%;border-collapse:collapse;">
                    <thead>
                        <tr style="background:#e8f0fe;">
                            <th style="padding:10px;text-align:left;color:#1a73e8;">#</th>
                            <th style="padding:10px;text-align:left;color:#1a73e8;">Asunto / Remitente</th>
                            <th style="padding:10px;text-align:left;color:#1a73e8;">Vista previa</th>
                        </tr>
                    </thead>
                    <tbody>{filas_html}</tbody>
                </table>'''
    }
            </div>

            <!-- Pie -->
            <div style="background:#f8f9fa;padding:16px 30px;text-align:center;
                        color:#aaa;font-size:12px;border-top:1px solid #eee;">
                Notificación automática generada por gmail_notificador.py
            </div>
        </div>
    </body>
    </html>
    """
    return html


# ─────────────────────────────────────────────
# FUNCIÓN: Enviar correo de notificación
# ─────────────────────────────────────────────


def enviar_notificacion(correos):
    """Envía el resumen de correos no leídos al correo destino."""
    total = len(correos)
    asunto_email = f"📬 Tienes {total} correo{'s' if total != 1 else ''} no leído{'s' if total != 1 else ''} en Gmail"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto_email
    msg["From"] = f"Notificador Gmail <{GMAIL_USER}>"
    msg["To"] = f"{DESTINO_NOMBRE} <{DESTINO_EMAIL}>"

    # Versión texto plano (fallback)
    texto_plano = f"Tienes {total} correo(s) no leído(s).\n\n"
    for i, c in enumerate(correos, 1):
        texto_plano += (
            f"{i}. [{c['asunto']}] de {c['de']}\n   {c['fecha']}\n   {c['preview']}\n\n"
        )

    # Versión HTML
    html = construir_html(correos)

    msg.attach(MIMEText(texto_plano, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    print(f"[INFO] Enviando notificación a {DESTINO_EMAIL}...")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            servidor.sendmail(GMAIL_USER, DESTINO_EMAIL, msg.as_string())
        print(f"[OK] Notificación enviada correctamente a {DESTINO_EMAIL}.")
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Autenticación SMTP fallida.")
        print(
            "  → Verifica tu App Password en: https://myaccount.google.com/apppasswords"
        )
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  Gmail Notificador")
    print("=" * 50)

    correos_no_leidos = leer_no_leidos()

    if correos_no_leidos:
        print(f"[INFO] Procesando {len(correos_no_leidos)} correo(s)...")
        enviar_notificacion(correos_no_leidos)
    else:
        print("[INFO] Sin correos no leídos. No se enviará notificación.")

    print("=" * 50)
    print("  Proceso finalizado.")
    print("=" * 50)
