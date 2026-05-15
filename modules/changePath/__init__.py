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
from time import sleep

"""
    Obtengo el modulo que fueron invocados
"""
module = GetParams("module")

"""
    Resuelvo catpcha tipo reCaptchav2
"""
if module == "change_":
    import os
    path_ = GetParams('path_')
    print('VARIABLE',path_)

    p_ = GetVar(path_)
    print(p_)
    var_ = GetParams('var_')

    print(path_, var_)

    p_ = p_.replace("\\",'/')
    print(p_)

    SetVar(var_,p_)
