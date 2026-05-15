"""
setup_proyecto.py
=================
Automatizacion de configuracion inicial del proyecto ConsultaJudicial.

Pasos que ejecuta:
    0. Instala dependencias necesarias (pywin32) si no estan instaladas.
    1. Crea la variable de entorno RUTA_BD de forma permanente (setx).
    2. Valida que la variable quedo registrada.
    3. Valida si la ruta destino existe; si no, la crea.
    4. Clona el repositorio ConsultaJudicial en la ruta destino.
    5. Valida que el repositorio fue clonado correctamente.
    6. Guarda las credenciales de Gmail en el Administrador de Credenciales de Windows.
    7. Valida que las credenciales fueron guardadas correctamente.

Requisitos:
    - Python 3.7+
    - Git instalado y disponible en el PATH del sistema.
    - Ejecutar con permisos de usuario (no requiere administrador).
"""

import os
import subprocess
import sys
from pathlib import Path

# ─────────────────────────────────────────────
# DEPENDENCIAS — no modificar
# ─────────────────────────────────────────────

DEPENDENCIAS = [
    ("win32cred", "pywin32"),  # (modulo a importar, paquete pip a instalar)
]

# ─────────────────────────────────────────────
# CONFIGURACION — edita estos valores
# ─────────────────────────────────────────────

NOMBRE_VARIABLE = "RUTA_BD"
VALOR_VARIABLE = r"C:/roc_studio/Proyectos/Main_ConsultaJudicial/resources/datos.db"
RUTA_DESTINO = Path(r"C:/roc_studio/Proyectos")
REPO_URL = "https://github.com/JononathanRincon/ConsultaJudicial.git"
NOMBRE_REPO = "Main_ConsultaJudicial"

# Credenciales Gmail — edita estos valores
GMAIL_TARGET = (
    "Gmail_ConsultaJudicial"  # Nombre clave en el Administrador de Credenciales
)
GMAIL_USUARIO = "jonathandevrpa@gmail.com"  # Tu cuenta Gmail
GMAIL_PASSWORD = "kigo wmub ndpk qwmj"  # App Password de Google (16 caracteres)


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────


def separador(titulo=""):
    ancho = 55
    print("\n" + "-" * ancho)
    if titulo:
        print(f"  {titulo}")
        print("-" * ancho)


def ok(msg):
    print(f"  [OK] {msg}")


def info(msg):
    print(f"  [->] {msg}")


def error(msg):
    print(f"  [!!] {msg}")


# ─────────────────────────────────────────────
# PASO 0: Instalar dependencias automaticamente
# ─────────────────────────────────────────────


def instalar_dependencias():
    separador("PASO 0 — Verificar e instalar dependencias")

    for modulo, paquete in DEPENDENCIAS:
        info(f"Verificando '{paquete}'...")
        try:
            __import__(modulo)
            ok(f"'{paquete}' ya esta instalado.")
        except ImportError:
            info(f"'{paquete}' no encontrado. Instalando con pip...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", paquete, "--quiet"],
                    check=True,
                )
                ok(f"'{paquete}' instalado correctamente.")

                # Verificar que quedo bien instalado
                try:
                    __import__(modulo)
                    ok(f"'{paquete}' verificado y listo para usar.")
                except ImportError:
                    error(f"'{paquete}' se instalo pero no se puede importar.")
                    error("Intenta reiniciar el terminal y volver a ejecutar.")
                    sys.exit(1)

            except subprocess.CalledProcessError:
                error(f"No se pudo instalar '{paquete}' automaticamente.")
                error(f"Ejecuta manualmente: pip install {paquete}")
                sys.exit(1)


# ─────────────────────────────────────────────
# PASO 1: Crear variable de entorno permanente
# ─────────────────────────────────────────────


def crear_variable_entorno():
    separador("PASO 1 — Crear variable de entorno")
    info(f"Nombre  : {NOMBRE_VARIABLE}")
    info(f"Valor   : {VALOR_VARIABLE}")

    os.environ[NOMBRE_VARIABLE] = VALOR_VARIABLE

    try:
        subprocess.run(
            ["setx", NOMBRE_VARIABLE, VALOR_VARIABLE],
            capture_output=True,
            text=True,
            check=True,
        )
        ok("Variable de entorno guardada permanentemente con setx.")
        info("Nota: Estara disponible en nuevos procesos/terminales.")
    except FileNotFoundError:
        error("Comando 'setx' no encontrado. Estas en Windows?")
        error("La variable fue creada solo para esta sesion.")
    except subprocess.CalledProcessError as e:
        error(f"Error al ejecutar setx: {e.stderr.strip()}")
        sys.exit(1)


# ─────────────────────────────────────────────
# PASO 2: Validar que la variable existe
# ─────────────────────────────────────────────


def validar_variable_entorno():
    separador("PASO 2 — Validar variable de entorno")

    valor = os.environ.get(NOMBRE_VARIABLE)

    if valor:
        ok(f"Variable '{NOMBRE_VARIABLE}' encontrada.")
        ok(f"Valor   : {valor}")
    else:
        error(f"Variable '{NOMBRE_VARIABLE}' NO encontrada en el entorno.")
        error("Revisa el Paso 1 o reinicia el terminal y vuelve a ejecutar.")
        sys.exit(1)


# ─────────────────────────────────────────────
# PASO 3: Validar/crear ruta destino
# ─────────────────────────────────────────────


def preparar_ruta_destino():
    separador("PASO 3 — Validar ruta destino")
    info(f"Ruta: {RUTA_DESTINO}")

    if RUTA_DESTINO.exists():
        ok("La ruta destino ya existe.")
    else:
        info("La ruta no existe. Creando directorios...")
        try:
            RUTA_DESTINO.mkdir(parents=True, exist_ok=True)
            ok(f"Ruta creada: {RUTA_DESTINO}")
        except PermissionError:
            error("Sin permisos para crear la ruta.")
            error("Intenta ejecutar el script como administrador.")
            sys.exit(1)
        except Exception as e:
            error(f"No se pudo crear la ruta: {e}")
            sys.exit(1)


# ─────────────────────────────────────────────
# PASO 4: Clonar el repositorio
# ─────────────────────────────────────────────


def clonar_repositorio():
    separador("PASO 4 — Clonar repositorio")

    ruta_repo = RUTA_DESTINO / NOMBRE_REPO
    info(f"Repositorio : {REPO_URL}")
    info(f"Destino     : {ruta_repo}")

    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        error("Git no esta instalado o no esta en el PATH.")
        error("Descargalo en: https://git-scm.com/downloads")
        sys.exit(1)

    if ruta_repo.exists():
        git_dir = ruta_repo / ".git"
        if git_dir.exists():
            ok(f"El proyecto '{NOMBRE_REPO}' ya existe en:")
            ok(f"  {ruta_repo}")
            ok("No se realizara la clonacion para evitar duplicados.")
            try:
                rama = subprocess.run(
                    ["git", "-C", str(ruta_repo), "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip()
                commit = subprocess.run(
                    ["git", "-C", str(ruta_repo), "log", "--oneline", "-1"],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip()
                info(f"Rama activa  : {rama}")
                info(f"Ultimo commit: {commit}")
            except subprocess.CalledProcessError:
                info("No se pudo obtener informacion del repositorio.")
            return
        else:
            error(
                f"La carpeta '{NOMBRE_REPO}' ya existe pero NO es un repositorio git valido."
            )
            error(f"Ruta: {ruta_repo}")
            error("  1. Elimina la carpeta manualmente y vuelve a ejecutar.")
            error("  2. Verifica si el proyecto fue descargado de otra forma.")
            sys.exit(1)

    info("Iniciando clonacion... (puede tardar unos segundos)")
    try:
        subprocess.run(["git", "clone", REPO_URL, str(ruta_repo)], check=True)
        ok("Repositorio clonado exitosamente.")
    except subprocess.CalledProcessError as e:
        error(f"Error al clonar el repositorio: {e}")
        error("Verifica la URL y tu conexion a internet.")
        sys.exit(1)


# ─────────────────────────────────────────────
# PASO 5: Validar que el repositorio quedo bien
# ─────────────────────────────────────────────


def validar_repositorio():
    separador("PASO 5 — Validar repositorio clonado")

    ruta_repo = RUTA_DESTINO / NOMBRE_REPO

    if not ruta_repo.exists():
        error(f"La carpeta del repositorio no existe: {ruta_repo}")
        sys.exit(1)

    git_dir = ruta_repo / ".git"
    if not git_dir.exists():
        error("La carpeta no contiene un repositorio git valido.")
        sys.exit(1)

    ok(f"Repositorio encontrado en: {ruta_repo}")
    archivos = list(ruta_repo.iterdir())
    info(f"Archivos/carpetas en el repositorio ({len(archivos)}):")
    for archivo in sorted(archivos):
        tipo = "[DIR]" if archivo.is_dir() else "[DOC]"
        print(f"       {tipo} {archivo.name}")


# ─────────────────────────────────────────────
# PASO 6: Guardar credenciales Gmail en
#         Administrador de Credenciales Windows
# ─────────────────────────────────────────────


def guardar_credenciales_gmail():
    separador("PASO 6 — Guardar credenciales Gmail")
    info(f"Nombre clave : {GMAIL_TARGET}")
    info(f"Usuario      : {GMAIL_USUARIO}")
    info(f"Password     : {'*' * len(GMAIL_PASSWORD)}")

    import win32cred
    import pywintypes

    try:
        credencial = {
            "Type": win32cred.CRED_TYPE_GENERIC,
            "TargetName": GMAIL_TARGET,
            "UserName": GMAIL_USUARIO,
            "CredentialBlob": GMAIL_PASSWORD,
            "Persist": win32cred.CRED_PERSIST_LOCAL_MACHINE,
            "Comment": "Credenciales Gmail para proyecto ConsultaJudicial",
        }
        win32cred.CredWrite(credencial, 0)
        ok(f"Credencial '{GMAIL_TARGET}' guardada en el Administrador de Credenciales.")
        ok(f"Usuario  : {GMAIL_USUARIO}")
        ok("Password : guardado de forma segura.")
    except pywintypes.error as e:
        error(f"Error al guardar credencial: {e}")
        sys.exit(1)


# ─────────────────────────────────────────────
# PASO 7: Validar que las credenciales existen
# ─────────────────────────────────────────────


def validar_credenciales_gmail():
    separador("PASO 7 — Validar credenciales Gmail")

    import win32cred
    import pywintypes

    try:
        cred = win32cred.CredRead(GMAIL_TARGET, win32cred.CRED_TYPE_GENERIC)
        ok(f"Credencial '{GMAIL_TARGET}' encontrada correctamente.")
        ok(f"Usuario guardado: {cred['UserName']}")
    except pywintypes.error:
        error(f"Credencial '{GMAIL_TARGET}' NO encontrada.")
        error(
            "Revisa el Paso 6 o verifica el Administrador de Credenciales de Windows."
        )
        sys.exit(1)


# ─────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────


def resumen_final():
    separador("CONFIGURACION COMPLETADA")
    ok(f"Variable de entorno : {NOMBRE_VARIABLE} = {VALOR_VARIABLE}")
    ok(f"Ruta del proyecto   : {RUTA_DESTINO / NOMBRE_REPO}")
    ok(f"Repositorio         : {REPO_URL}")
    ok(f"Credencial Gmail    : {GMAIL_TARGET} ({GMAIL_USUARIO})")
    print()
    info("Proximos pasos:")
    print("    1. Abre Rocketbot Studio.")
    print(f"    2. Carga el proyecto desde: {RUTA_DESTINO / NOMBRE_REPO}")
    print()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("=" * 55)
    print("   Setup - Proyecto ConsultaJudicial")
    print("=" * 55)

    instalar_dependencias()  # PASO 0 — siempre primero
    crear_variable_entorno()  # PASO 1
    validar_variable_entorno()  # PASO 2
    preparar_ruta_destino()  # PASO 3
    clonar_repositorio()  # PASO 4
    validar_repositorio()  # PASO 5
    guardar_credenciales_gmail()  # PASO 6
    validar_credenciales_gmail()  # PASO 7
    resumen_final()

    print("=" * 55)
