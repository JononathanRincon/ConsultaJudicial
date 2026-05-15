# coding: utf-8
import json
import os
import sys
import traceback
from datetime import datetime
import ssl

BASE_PATH = tmp_global_obj["basepath"]  # type: ignore
module_path = os.path.join(BASE_PATH, "modules", "ModulesToolsFCV", "libs")  # type: ignore
if module_path not in sys.path:
    sys.path.append(module_path)
import pyodbc
import keyring
import socket
import smtplib
import importlib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.message import EmailMessage

import email_templates  # type: ignore

importlib.reload(email_templates)

global log, logger_config, inicializar_logger, escribir_log


def log(mensaje: str, tipo: str = "INFO"):
    import datetime

    colores = {
        "INFO": "\033[94m",  # Azul
        "WARNING": "\033[93m",  # Amarillo
        "ERROR": "\033[91m",  # Rojo
        "DEBUG": "\033[92m",  # Verde
        "ENDC": "\033[0m",  # Fin color
    }

    tipo = tipo.upper()
    color = colores.get(tipo, colores["INFO"])
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mensaje_formateado = f"{ahora} {color}[{tipo}]{colores['ENDC']} - {mensaje}"
    print(mensaje_formateado)


module = GetParams("module")  # type: ignore
if module == "Config":
    try:
        """
        Conecta a la base de datos SQL Server usando credenciales seguras desde Windows Credential Manager
        y retorna un diccionario con las variables de configuración del bot, incluyendo el ambiente actual.
        """
        strNameTable = GetParams("txtNameTable")  # type: ignore
        log(f"{strNameTable}")  # type: ignore
        # Obtener credencial del sistema
        cred = keyring.get_credential("BOT01_RF_BDSQLSERVER", "")
        if cred is None:
            raise Exception(f"No se encontró la credencial: BOT01_RF_BDSQLSERVER")

        # Parsear JSON desde keyring
        datos_cred = json.loads(cred.password)

        # Armar cadena de conexión
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={datos_cred['servidor']};"
            f"DATABASE={datos_cred['base_datos']};"
            f"UID={datos_cred['usuario']};"
            f"PWD={datos_cred['contrasena']};"
            f"Trusted_Connection=no;"
        )

        # Conectar
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        log("Conectado a la Base de datos")
        # Consulta SQL: Config + Ambiente
        sql = f"""
            SELECT 
                Name,
                CASE 
                    WHEN (SELECT Prod FROM {strNameTable} WHERE Name = 'Produccion') = 'True' THEN Prod 
                    ELSE Dev 
                END AS ValorConfiguracion,
                CASE 
                    WHEN (SELECT Prod FROM {strNameTable} WHERE Name = 'Produccion') = 'True' THEN 'Prod'
                    ELSE 'Dev'
                END AS Ambiente
            FROM {strNameTable} ORDER BY Id;
        """
        cursor.execute(sql)
        log("Query Config Realizado")
        # Armar diccionario de configuración
        dctVars = {}
        ambiente = None
        for row in cursor.fetchall():
            nombre = row.Name
            valor = row.ValorConfiguracion
            ambiente = row.Ambiente  # se repetirá, pero es el mismo
            dctVars[nombre] = valor
        dctVars["Ambiente"] = ambiente
        log("Variable de configuracion realizada")
        conn.close()

        strConfigLog = GetParams("cbxConfigLog")  # type: ignore

        if strConfigLog == "True":
            # 1. Fecha actual en formato YYYYMMDD
            dteFechaActual = datetime.now().strftime("%Y%m%d")
            # 2. Año, mes, día
            strAnio = dteFechaActual[:4]
            strMes = dteFechaActual[4:6]
            strDia = dteFechaActual[6:8]

            # 3. Simulación del diccionario con ruta base (esto ya viene de la config real)
            # Por ejemplo: dctVars = obtener_configuracion_bot()
            # Aquí te muestro un ejemplo para test:
            # dctVars = {"PathLogs": "C:/RadicacionFacturasFCV/Tracing/Logs"}

            # Asegúrate de que PathLogs esté normalizado y sin barra final
            ruta_base = dctVars["PathLogs"].rstrip("/\\")  # type: ignore
            codBot = dctVars["CodBot"]  # type: ignore
            usuario = os.getlogin()
            maquina = socket.gethostname()
            # 4. Construir ruta final del log del día
            ruta_completa_log = os.path.join(
                ruta_base,  # type: ignore
                strAnio,
                strMes,
                f"Log_{codBot}_{dteFechaActual}_{maquina.capitalize()}_{usuario.capitalize()}.txt",
            )

            # 5. Crear carpetas si no existen
            os.makedirs(os.path.dirname(ruta_completa_log), exist_ok=True)

            # 6. Asignar la ruta final al diccionario de configuración
            dctVars["PathLogs"] = ruta_completa_log
            log("Se almacena la ruta completa del log")
            if not os.path.exists(ruta_completa_log):
                try:
                    with open(ruta_completa_log, "w") as f:
                        f.write("")  # Crea un archivo vacío
                    log(f"Archivo '{ruta_completa_log}")
                except Exception as e:
                    print(f"Error al crear el archivo: {e}")
            else:
                log(f"El archivo '{ruta_completa_log}' ya existe.")
        SetVar("dctVars", dctVars)  # type: ignore
    except Exception as e:
        error_info = traceback.format_exc()
        log(f"Error al obtener configuración del bot: {str(e)}{error_info}", "ERROR")
        SetVar("MensajeError", f"{str(e)} | Traceback: {error_info}")
        raise e

global get_file_paths


def get_file_paths(param):
    if not param:
        return []

    param = param.strip()

    # Quitar corchetes [ ] si existen
    if param.startswith("[") and param.endswith("]"):
        param = param[1:-1]

    # Separar por comas
    parts = param.split(",")

    # Limpiar cada parte (quitar comillas simples/dobles y espacios extra)
    files = [p.strip().strip("'").strip('"') for p in parts if p.strip()]

    return files


if module == "Notificaciones":
    try:
        # ------------------ Recuperar parámetros del paquete (proporcionados por Rocketbot) ------------------
        smtp_user = (GetParams("txtUser") or "").strip()
        smtp_password = (GetParams("txtPasword") or "").strip()
        smtp_port = int(GetParams("txtPuerto"))
        smtp_server = GetParams("txtServer")
        tipo_notificacion = GetParams("cbxTipoAtencion")
        nombre_bot = GetParams("txtNameBot")
        remitente = (GetParams("txtRemitente") or "").strip()
        cc = (GetParams("txtCc") or "").strip()
        bcc = (GetParams("txtCopiaOculta") or "").strip()
        ruta_log = GetParams("txtPathLog")
        attached_files = get_file_paths(GetParams("PathFile"))
        total_procesados = int(GetParams("txtTotalProcesados") or 0)
        total_exitosos = int(GetParams("txtRegistrosExitosos") or 0)
        total_fallidos = int(GetParams("txtRegistrosFallos") or 0)
        descripcion_error = GetParams("txtError")
        ambiente = GetParams("txtAmbienteProduccion")
        disable_ssl_verification = GetParams("blnHabilitarSsl")
        ModificarAsunto = GetParams("blnModificarAsunto")
        ModificarCuerCorreo = GetParams("blnModificarCuerpoCorreo")
        MensajeAsunto = GetParams("txtMensajeAsunto")
        CuerpoMensaje = GetParams("txtCuerpoMensaje")
        TypeAlerta = GetParams("txtAlerta")
        log(f"remitente: {remitente}, cc: {cc}, bcc: {bcc}", "DEBUG")
        if disable_ssl_verification is None:
            disable_ssl_verification = "False"
        # ------------------ Variables base del sistema ------------------
        usuario = os.getlogin()
        maquina = socket.gethostname()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ano = str(datetime.now().year)
        log("Variables del sistema cargadas correctamente", "INFO")

        # ------------------ Template HTML según tipo de notificación (proporcionado por Rocketbot) ------------------
        html = ""  # Inicializar variable html
        subject = ""  # Inicializar variable subject

        if tipo_notificacion == "Inicio":
            subject = f"Inicio Bot - {nombre_bot}"
            html = email_templates.correoInicio.format(
                NombreBot=nombre_bot,
                FechaInicio=fecha_actual,
                Ambiente=ambiente,
                Usuario=usuario,
                Maquina=maquina,
                RutaLog=ruta_log,
                Ano=ano,
            )
        elif tipo_notificacion == "Fin":
            subject = f"Finalizacion Bot - {nombre_bot}"
            html = email_templates.MensajeFin.format(
                NombreBot=nombre_bot,
                FechaFin=fecha_actual,
                TotalProcesados=total_procesados,
                TotalExitosos=total_exitosos,
                TotalFallidos=total_fallidos,
                RutaLog=ruta_log,
                Ambiente=ambiente,
                Usuario=usuario,
                Maquina=maquina,
                Ano=ano,
            )
        elif tipo_notificacion == "Novedad":
            subject = f"Novedad en ejecucion Bot - {nombre_bot}"
            html = email_templates.NotificacionError.format(
                NombreBot=nombre_bot,
                FechaEvento=fecha_actual,
                TipoAlerta=TypeAlerta,
                DescripcionAlerta=descripcion_error,
                RutaLog=ruta_log,
                Ambiente=ambiente,
                Usuario=usuario,
                Maquina=maquina,
                Ano=ano,
            )
        elif tipo_notificacion == "Notificacion":
            if ModificarAsunto == "True":
                if MensajeAsunto == None:
                    raise ValueError(
                        "ModificarAsunto es True, pero MensajeAsunto está vacío."
                    )
                subject = MensajeAsunto
            else:
                subject = f"Resumen ejecucion Bot - {nombre_bot}"

            if ModificarCuerCorreo == "True":
                if CuerpoMensaje == None:
                    log(
                        f"No se ingresó el mensaje del cuerpo del correo, se usará el mensaje por defecto.",
                        "WARNING",
                    )
                    raise ValueError("No se ingresó el mensaje del cuerpo del correo.")
                else:
                    html = email_templates.MensajeEnvioNotificacion.format(
                        NombreBot=nombre_bot, MensajeEnvio=CuerpoMensaje, Ano=ano
                    )
            else:
                html = email_templates.MensajeEnvioNotificacion.format(
                    NombreBot=nombre_bot, Ano=ano, MensajeEnvio=""
                )

        else:
            raise ValueError("Tipo de notificación no reconocido.")

        log("Template HTML seleccionado y formateado.", "INFO")

        # ------------------ Construcción del Correo (EmailMessage) ------------------
        def split_emails(emails_str):
            return (
                [email.strip() for email in emails_str.split(",") if email.strip()]
                if emails_str
                else []
            )

        destinatarios_to = split_emails(remitente)
        destinatarios_cc = split_emails(cc)
        destinatarios_bcc = split_emails(bcc)
        todos_los_destinatarios = (
            destinatarios_to + destinatarios_cc + destinatarios_bcc
        )

        # Creamos una instancia de EmailMessage
        msg = EmailMessage()
        msg["From"] = smtp_user
        msg["To"] = ", ".join(destinatarios_to)
        msg["Cc"] = ", ".join(destinatarios_cc)
        # EmailMessage maneja automáticamente la codificación UTF-8 para el asunto
        msg["Subject"] = str(Header(subject, charset="utf-8"))

        # Adjuntar cuerpo del correo (HTML)
        # set_content maneja automáticamente el tipo MIME y la codificación
        msg.set_content(html, subtype="html", charset="utf-8")

        # ------------------ Adjuntar Logos (inline) ------------------
        # La ruta a los logos
        ruta_directorio = os.path.dirname(os.path.abspath(__file__))

        for cid_tag, filename in [("logoFCV", "fcv.png")]:
            ruta_logo = os.path.join(
                ruta_directorio, "modules", "ModulesToolsFCV", "img", filename
            )
            if os.path.isfile(ruta_logo):
                try:
                    with open(ruta_logo, "rb") as f:
                        # add_attachment para imágenes inline. content_id es el CID.
                        msg.add_attachment(
                            f.read(), maintype="image", subtype="png", cid=cid_tag
                        )
                    log(f"Logo {filename} adjuntado inline con CID: {cid_tag}.", "INFO")
                except Exception as e:
                    log(f"No se pudo adjuntar el logo {filename}: {e}", "WARNING")
            else:
                log(f"No se encontró la imagen del logo: {ruta_logo}", "WARNING")

        # ------------------ Adjuntar Archivo (si existe) ------------------
        for file_path in attached_files:
            if os.path.exists(file_path):
                try:
                    filename = os.path.basename(file_path)
                    with open(file_path, "rb") as f:
                        msg.add_attachment(
                            f.read(),
                            maintype="application",
                            subtype="octet-stream",
                            filename=filename,
                        )
                    log(f"Archivo adjuntado: {filename}", "INFO")
                except Exception as e:
                    log(f"Error al adjuntar el archivo {file_path}: {e}", "ERROR")
            else:
                log(f"No se encontró el archivo: {file_path}", "WARNING")

        # ------------------ Conexión y Envío ------------------
        log(f"Intentando conectar al servidor Correo FCV...", "INFO")
        # Usamos un contexto SSL/TLS para una conexión segura
        context = ssl.create_default_context()

        # Si se selecciona la opción de deshabilitar la verificación SSL
        if disable_ssl_verification:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            log(
                "ADVERTENCIA: La verificación de certificados SSL ha sido deshabilitada. Esto reduce la seguridad.",
                "WARNING",
            )

        try:
            # Usamos SMTP con starttls para el puerto 587
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # server.set_debuglevel(1) # Activa logs de depuración para ver la conversación SMTP
                server.starttls(context=context)  # Usar el contexto SSL/TLS
                server.login(smtp_user, smtp_password)
                # send_message es el método recomendado para EmailMessage
                server.send_message(msg)
                log("Correo enviado exitosamente.", "INFO")
        except smtplib.SMTPAuthenticationError as e:
            log(
                f"Error de autenticación SMTP: {e}. Verifica usuario y contraseña (o contraseña de aplicación).",
                "ERROR",
            )
            raise e
        except smtplib.SMTPException as e:
            log(f"Error SMTP al enviar el correo: {e}", "ERROR")
            raise e
        except Exception as e:
            log(f"Error inesperado durante el envío del correo: {e}", "ERROR")
            raise e

        SetVar("blnValidadEnvioCorreo", True)

    except ValueError as ve:
        error_info = traceback.format_exc()
        log(f"Error en módulo Notificaciones: {str(ve)}\n{error_info}", "ERROR")
        SetVar("MensajeError", f"{str(ve)} | Traceback: {error_info}")
        SetVar("blnValidadEnvioCorreo", False)
        raise ve

    except Exception as e:
        error_info = traceback.format_exc()
        log(f"Error en módulo Notificaciones: {str(e)}\n{error_info}", "ERROR")
        SetVar("MensajeError", f"{str(e)} | Traceback: {error_info}")
        SetVar("blnValidadEnvioCorreo", False)
        raise e

# ---------------- CONFIGURACIÓN GLOBAL ----------------
logger_config = {"ruta_log": None, "usar_logging": False}


def inicializar_logger(ruta_log, usar_logging=True):
    import logging

    log(f"Ruta del archivo {ruta_log}")
    logger_config["ruta_log"] = ruta_log
    logger_config["usar_logging"] = usar_logging
    # Limpieza de handlers previos
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if usar_logging:
        os.makedirs(os.path.dirname(ruta_log), exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(ruta_log, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )


def escribir_log(mensaje, nivel="info", usar_logger=True):
    import logging

    if logger_config["usar_logging"] and usar_logger:
        getattr(logging, nivel.lower(), logging.info)(mensaje)
    else:
        linea = str(mensaje)
        ruta = logger_config["ruta_log"]
        if ruta:
            with open(ruta, "a", encoding="utf-8") as f:
                f.write(linea + "\n")
                f.close()
        # También coloreo consola
        log(linea, tipo=nivel)


# ---------------- EJECUCIÓN MÓDULO ROCKETBOT ----------------
module = GetParams("module")
if module == "ModulesLogs":
    import logging

    try:
        ruta = GetParams("PathLog") or ""
        if not ruta:
            raise Exception("No se ha configurado la ruta del archivo de log.")
        inicializar_logger(ruta, usar_logging=True)

        action = GetParams("cbxLogActionType")
        nivel = (GetParams("cbxNivelLog") or "info").lower()
        bot = GetParams("txtNameBot")
        hu = GetParams("txtNameHU")
        msg = GetParams("txtMensajeLog")

        if action == "StartMain":
            if not bot:
                raise ValueError("Falta txtNameBot")
            escribir_log("-" * 56, usar_logger=False)
            escribir_log(
                f"Inicio Ejecucion del Bot {bot} {datetime.now():%Y-%m-%d %H:%M:%S}",
                usar_logger=False,
            )
            escribir_log("-" * 56, usar_logger=False)

        elif action == "EndMain":
            if not bot:
                raise ValueError("Falta txtNameBot")
            escribir_log("-" * 56, usar_logger=False)
            escribir_log(
                f"Finalizo Ejecucion del Bot {bot} - {datetime.now():%Y-%m-%d %H:%M:%S}",
                usar_logger=False,
            )
            escribir_log("-" * 56, usar_logger=False)

        elif action == "StartHU":
            if not hu:
                raise ValueError("Falta Ingresa el nombre de la HU o FUN")
            escribir_log(
                f"------- Inicio de la ejecucion de {hu} -------",
                nivel=nivel,
                usar_logger=True,
            )

        elif action == "EndHU":
            if not hu:
                raise ValueError("Falta Ingresa el nombre de la HU o FUN")
            escribir_log(
                f"------- Finalizo la ejecucion de {hu} -------",
                nivel=nivel,
                usar_logger=True,
            )

        elif action == "StartFUN":
            if not hu:
                raise ValueError("Falta Ingresa el nombre de la HU o FUN")
            escribir_log(f"Inicio de la ejecucion {hu}", nivel=nivel, usar_logger=True)

        elif action == "EndFUN":
            if not hu:
                raise ValueError("Falta Ingresa el nombre de la HU o FUN")
            escribir_log(f"Finalizo la ejecucion {hu}", nivel=nivel, usar_logger=True)

        elif action == "MensageTrace":
            if not msg:
                raise ValueError("Falta txtMensajeLog para mensaje")
            escribir_log(msg, nivel=nivel, usar_logger=True)

        else:
            raise ValueError(f"Acción no reconocida: {action}")

        SetVar("blnLogRegistrado", True)
        logging.shutdown()
    except Exception as e:
        error_info = traceback.format_exc()
        # Uso escribir_log para que quede en txt y consola coloreada
        escribir_log(
            f"ERROR al registrar el log: {e} - {error_info}",
            nivel="error",
            usar_logger=False,
        )
        SetVar("MensajeError", f"{e} | Trace: {error_info}")
        SetVar("blnLogRegistrado", False)
        logging.shutdown()
        raise e
