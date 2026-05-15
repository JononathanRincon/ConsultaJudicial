# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

"""
    Obtengo el modulo que fue invocado
"""

base_path  = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'WindowsCredentialManager' + os.sep + 'libs' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)

from typing import Tuple
import ctypes as CT
import ctypes.wintypes as WT


global WT
CRED_TYPE_GENERIC = 0x01
LPBYTE = CT.POINTER(WT.BYTE)
LPWSTR = WT.LPWSTR
LPCWSTR = WT.LPWSTR


class CREDENTIAL_ATTRIBUTE(CT.Structure):
    global LPWSTR, LPBYTE, LPCWSTR
    _fields_ = [
        ('Keyword', LPWSTR),
        ('Flags', WT.DWORD),
        ('ValueSize', WT.DWORD),
        ('Value', LPBYTE)]


PCREDENTIAL_ATTRIBUTE = CT.POINTER(CREDENTIAL_ATTRIBUTE)


class CREDENTIAL(CT.Structure):
    global LPWSTR, LPBYTE, LPCWSTR, PCREDENTIAL_ATTRIBUTE
    _fields_ = [
        ('Flags', WT.DWORD),
        ('Type', WT.DWORD),
        ('TargetName', LPWSTR),
        ('Comment', LPWSTR),
        ('LastWritten', WT.FILETIME),
        ('CredentialBlobSize', WT.DWORD),
        ('CredentialBlob', LPBYTE),
        ('Persist', WT.DWORD),
        ('AttributeCount', WT.DWORD),
        ('Attributes', PCREDENTIAL_ATTRIBUTE),
        ('TargetAlias', LPWSTR),
        ('UserName', LPWSTR)]


PCREDENTIAL = CT.POINTER(CREDENTIAL)
advapi32 = CT.WinDLL('Advapi32.dll')
advapi32.CredReadA.restype = WT.BOOL
advapi32.CredReadA.argtypes = [LPCWSTR, WT.DWORD, WT.DWORD, CT.POINTER(PCREDENTIAL)]


def GetGenericCredential(name: str) -> Tuple[str, str]:
    """
    Returns a Tuple of Name and Password of a Generic Windows Credential
    Uses bytes in Py3 and str in Py2 for url, name and password.
    """
    global PCREDENTIAL, advapi32, CRED_TYPE_GENERIC, CT
    cred_ptr = PCREDENTIAL()
    if advapi32.CredReadW(name, CRED_TYPE_GENERIC, 0, CT.byref(cred_ptr)):
        username = cred_ptr.contents.UserName
        cred_blob = cred_ptr.contents.CredentialBlob
        cred_blob_size = cred_ptr.contents.CredentialBlobSize
        cred_str = CT.string_at(cred_blob, cred_blob_size)
        password = cred_str.decode('utf-16le', errors='ignore')
        advapi32.CredFree(cred_ptr)
        return username, password
    else:
        raise IOError("Failure reading credential")

module = GetParams("module")


if module == "getCredentials":
    name = GetParams("name_")
    var = GetParams("var_")
    pass_ = GetParams("pass_")
    try:
        name, pwd = GetGenericCredential(name)
        if var:
            SetVar(var, name)
            SetVar(pass_, pwd)

    except Exception as e:
        PrintException()
        raise e

