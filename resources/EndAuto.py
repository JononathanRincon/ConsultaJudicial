"""
cleanup_proyecto.py
===================
Elimina la configuracion del proyecto ConsultaJudicial.

Pasos que ejecuta:
    1. Elimina la variable de entorno RUTA_BD del registro de Windows.
    2. Elimina la variable del proceso actual.
    3. Valida que la variable fue eliminada correctamente.
    4. Elimina la credencial Gmail del Administrador de Credenciales de Windows.
    5. Valida que la credencial fue eliminada correctamente.

Requisitos:
    - Python 3.7+
    - pywin32 instalado (pip install pywin32)
"""

import os
import subprocess
import sys

# ─────────────────────────────────────────────
# CONFIGURACION — debe coincidir con setup_proyecto.py
# ─────────────────────────────────────────────

NOMBRE_VARIABLE = "RUTA_BD"
GMAIL_TARGET = (
    "Gmail_ConsultaJudicial"  # Nombre clave en el Administrador de Credenciales
)


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
# PASO 1 y 2: Eliminar variable de entorno
# ─────────────────────────────────────────────


def eliminar_variable_entorno():
    separador("PASO 1 — Eliminar variable de entorno")
    info(f"Variable : {NOMBRE_VARIABLE}")

    # Eliminar del registro de Windows (permanente)
    try:
        subprocess.run(
            ["reg", "delete", "HKCU\\Environment", "/v", NOMBRE_VARIABLE, "/f"],
            capture_output=True,
            text=True,
            check=True,
        )
        ok(f"Variable '{NOMBRE_VARIABLE}' eliminada del registro de Windows.")
    except subprocess.CalledProcessError:
        info(
            f"La variable '{NOMBRE_VARIABLE}' no existia en el registro. Continuando..."
        )

    # Eliminar del proceso actual
    os.environ.pop(NOMBRE_VARIABLE, None)
    ok(f"Variable '{NOMBRE_VARIABLE}' eliminada del proceso actual.")


# ─────────────────────────────────────────────
# PASO 3: Validar que la variable fue eliminada
# ─────────────────────────────────────────────


def validar_eliminacion_variable():
    separador("PASO 2 — Validar eliminacion de variable")

    # Verificar en el registro de Windows
    resultado = subprocess.run(
        ["reg", "query", "HKCU\\Environment", "/v", NOMBRE_VARIABLE],
        capture_output=True,
        text=True,
    )

    if resultado.returncode != 0:
        ok(f"Variable '{NOMBRE_VARIABLE}' confirmada como eliminada del registro.")
    else:
        error(f"La variable '{NOMBRE_VARIABLE}' aun existe en el registro.")
        error("Intenta ejecutar el script como administrador.")
        sys.exit(1)

    # Verificar en el proceso actual
    if os.environ.get(NOMBRE_VARIABLE) is None:
        ok(
            f"Variable '{NOMBRE_VARIABLE}' confirmada como eliminada del proceso actual."
        )
    else:
        error(f"La variable '{NOMBRE_VARIABLE}' aun existe en el proceso actual.")
        sys.exit(1)


# ─────────────────────────────────────────────
# PASO 4: Eliminar credencial de Windows
# ─────────────────────────────────────────────


def eliminar_credencial_gmail():
    separador("PASO 3 — Eliminar credencial Gmail")
    info(f"Nombre clave : {GMAIL_TARGET}")

    try:
        import win32cred
        import pywintypes
    except ImportError:
        error("Libreria 'pywin32' no instalada.")
        error("Ejecuta: pip install pywin32")
        sys.exit(1)

    try:
        win32cred.CredDelete(GMAIL_TARGET, win32cred.CRED_TYPE_GENERIC)
        ok(f"Credencial '{GMAIL_TARGET}' eliminada del Administrador de Credenciales.")
    except pywintypes.error as e:
        # Codigo 1168 = elemento no encontrado
        if e.winerror == 1168:
            info(f"La credencial '{GMAIL_TARGET}' no existia. Continuando...")
        else:
            error(f"Error al eliminar credencial: {e}")
            sys.exit(1)


# ─────────────────────────────────────────────
# PASO 5: Validar que la credencial fue eliminada
# ─────────────────────────────────────────────


def validar_eliminacion_credencial():
    separador("PASO 4 — Validar eliminacion de credencial")

    try:
        import win32cred
        import pywintypes
    except ImportError:
        error("Libreria 'pywin32' no instalada.")
        sys.exit(1)

    try:
        win32cred.CredRead(GMAIL_TARGET, win32cred.CRED_TYPE_GENERIC)
        # Si llega aqui, la credencial AUN existe
        error(f"La credencial '{GMAIL_TARGET}' aun existe. No fue eliminada.")
        sys.exit(1)
    except pywintypes.error as e:
        if e.winerror == 1168:
            ok(f"Credencial '{GMAIL_TARGET}' confirmada como eliminada.")
        else:
            error(f"Error inesperado al validar: {e}")
            sys.exit(1)


# ─────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────


def resumen_final():
    separador("LIMPIEZA COMPLETADA")
    ok(f"Variable de entorno '{NOMBRE_VARIABLE}' eliminada.")
    ok(f"Credencial '{GMAIL_TARGET}' eliminada del Administrador de Credenciales.")
    print()
    info("Para volver a configurar el proyecto ejecuta:")
    print("       python InitAuto.py")
    print()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("=" * 55)
    print("   Cleanup - Proyecto ConsultaJudicial")
    print("=" * 55)

    eliminar_variable_entorno()  # PASO 1
    validar_eliminacion_variable()  # PASO 2
    eliminar_credencial_gmail()  # PASO 3
    validar_eliminacion_credencial()  # PASO 4
    resumen_final()

    print("=" * 55)
