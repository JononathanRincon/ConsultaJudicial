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

import sys
import time
import datetime as dt
import os
from pathlib import Path
import shutil
import subprocess
import glob


"""
    Obtengo el modulo que fueron invocados
"""

# FUNCTIONS

if sys.platform == 'darwin':
    def openFolder(path):
        subprocess.check_call(['open', '--', path])
elif sys.platform == 'linux':
    def openFolder(path):
        subprocess.check_call(['xdg-open', path])
elif sys.platform == 'win32':
    def openFolder(path):
        try:
            subprocess.check_call(['explorer', path])
        except:
            pass


def getfile():
    global tk, filedialog
    file_path = ""
    if _platform == 'darwin':
        alert_ = """osascript -e 'set aa to choose file'"""
        p = subprocess.Popen(alert_, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        file_path = str(output).replace(str(output).split(":")[0], "").replace(":", "/").replace("\\n", "")
        if file_path.endswith("'"):
            file_path = file_path[:-1]
    else:
        root = tk.Tk()
        root.title("Rocketbot - Seleccione un archivo")
        root.after(5000, lambda: root.focus_force())
        root.focus()
        root.wm_attributes("-topmost", 1)
        w = 300
        h = 400
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.geometry("300x0+%d+%d" % (x, y))
        root.update()
        file_path = filedialog.askopenfilename(parent=root, title='Rocketbot - Seleccione un archivo')
        root.destroy()
        sleep(1)
    return file_path


def get_folder():
    file_path = ""
    try:
        print(sys.platform)
        if sys.platform == 'darwin':
            alert_ = """osascript -e 'set aa to choose folder name'"""
            p = subprocess.Popen(alert_, stdout=subprocess.PIPE, shell=True)
            output, err = p.communicate()
            file_path = str(output).replace(str(output).split(":")[0], "").replace(":", "/").replace("\\n", "")
            if file_path.endswith("'"):
                file_path = file_path[:-1]
        elif sys.platform == "win32" or sys.platform == "win64":
            scr = """
              Dim strPath

strPath = SelectFolder( "" )
If strPath = vbNull Then
    WScript.WScript.StdOut.Write("")
Else
    WScript.StdOut.Write(strPath)
End If


Function SelectFolder( myStartFolder )
' This function opens a "Select Folder" dialog and will
' return the fully qualified path of the selected folder
'
' Argument:
'     myStartFolder    [string]    the root folder where you can start browsing;
'                                  if an empty string is used, browsing starts
'                                  on the local computer
'
' Returns:
' A string containing the fully qualified path of the selected folder
'
' Written by Rob van der Woude
' http://www.robvanderwoude.com

    ' Standard housekeeping
    Dim objFolder, objItem, objShell
    
    ' Custom error handling
    On Error Resume Next
    SelectFolder = vbNull

    ' Create a dialog object
    Set objShell  = CreateObject( "Shell.Application" )
    Set objFolder = objShell.BrowseForFolder( 0, "Select Folder", 0, myStartFolder )

    ' Return the path of the selected folder
    If IsObject( objfolder ) Then SelectFolder = objFolder.Self.Path

    ' Standard housekeeping
    Set objFolder = Nothing
    Set objshell  = Nothing
    On Error Goto 0
End Function"""
            with open("tmp.vbs", "w") as f:
                print(scr)
                f.write(scr)
                f.close()
                con = subprocess.Popen('cscript tmp.vbs //Nologo', shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                a = con.communicate()
                print("> ",a)
                file_path = str(a[0].decode()).replace("\\", "/")
        else:
            root = tk.Tk()
            root.title("Rocketbot - Seleccione una carpeta")
            root.after(5000, lambda: root.focus_force())
            root.focus()
            root.wm_attributes("-topmost", 1)
            w = 300
            h = 400
            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            root.geometry("300x0+%d+%d" % (x, y))
            root.update()
            file_path = filedialog.askdirectory(parent=root, title='Rocketbot - Seleccione una carpeta')
            root.destroy()
            time.sleep(1)

    except Exception as e:
        print(e)

    return file_path

def remove_readonly(func, path, _):
                "Clear the readonly bit and reattempt the removal"
                os.chmod(path, 0o0200)
                func(path)

module = GetParams("module")

try:

    if module == "openFolder":
        path = GetParams("path").replace("/", os.sep)
        result = GetParams('var_')
    
        try:
            if os.path.isdir(path):
                openFolder(path)
            elif os.path.isfile(path):
                path = os.sep.join(path.split(os.sep)[:-1])
                openFolder(path)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "openFile":
        path = GetParams("path")
        result = GetParams('var_')

        try:
            if sys.platform == 'darwin' or sys.platform == 'linux':
                subprocess.call(["open", path])
            else:
                path = os.path.realpath(path)
                os.startfile(path)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "getFile":
        result = GetParams("result")

        try:
            path = getfile()
            SetVar(result, path)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "getFolder":
        result = GetParams("result")
    
        try:
            path = get_folder()
            SetVar(result, path)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "delete":
        path = GetParams("path")
        result = GetParams('var_')
        
        try:
            shutil.rmtree(path, onerror=remove_readonly)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "deleteFile":
        path = GetParams('path')
        name = GetParams('name')
        result = GetParams('var_')
                            
        try:
            if os.path.isdir(path):
                for zippath in glob.iglob(os.path.join(path, name)):
                    os.chmod(zippath, 0o0200)
                    os.remove(zippath)
                SetVar(result, True)
            else:
                SetVar(result, False)
                raise Exception("The path does not exist")
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "readFile":
        file_ = GetParams('file_')
        encoding = GetParams('encoding') if GetParams('encoding') else 'latin-1'
        split = GetParams("split")
        var_ = GetParams('var_')

        try:
            if split is not None:
                split = eval(split)
            with open(file_, 'r', encoding=encoding) as f:
                if split:
                    output = f.readlines()
                else:
                    output = f.read()
                
            SetVar(var_, output)
    
        except Exception as e:
            SetVar(var_, False)
            PrintException()
            raise e
    
    
    if module == "createFolder":
    
        folder = GetParams('path')
        result = GetParams('var_')
        
        try:
            os.makedirs(folder)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "exists":
        path  = GetParams("path")
        result = GetParams("var_")
    
        try:
            exist = os.path.exists(path)
    
            if result:
                SetVar(result, exist)
        except Exception as e:
            PrintException()
            raise e
    
    if module == "renameFolder":
        result = GetParams("var_")
    
        # Just tested in Linux
        # After test in Windows, change the json data for compatibility
        # Problem in Windows: Do not split well. Uses '/' and not '\'. So, cannot split it with so.sep
        # Dunno why. Investigate
        
        ## Tested in Windows, it works well. See comments for more information about separation
    
        # It take the path where the folder is contain
        path = GetParams('path')
    
        #It gets splited
        # Use os.sep [change separator for os.sep ( e.g.: pathSplited = path.slpit(separator) => pathSpliter = path.split(os.sep))] only if does not take from choosing the folder
        # because choosing the folder it gets in linux os.sep ('/'). It uses python, so, it gets that way.
        # pathSplited = path.split(os.sep)
        separator = "/"
        pathSplited = path.split(separator)
    
        # Gets the new folder's name
        newFoldersName = GetParams('newFoldersName')
    
        # Change the last item of the array (path splited) and in the last position, replace the old name with the new one
        pathSplited[(len(pathSplited)-1)] = newFoldersName
    
        # It gets join into one path
        pathWithNewFolder = separator.join(pathSplited)
    
        try:
        
            #os.chdir(path) Rompe rockect :S
            
            # Method to rename the folder
            os.rename(path, pathWithNewFolder)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    
    if module == "listFiles":
        path = GetParams("path")
        var_ = GetParams("result")
        option = GetParams("option")
    
        def ext(x):
            return os.path.splitext(x)[::-1]

        if option == "date":
            files = sorted(Path(path).iterdir(), key=os.path.getmtime)
            paths = [file.name for file in files]
        elif option == "type":
            files = sorted(Path(path).iterdir(), key=ext)
            paths = [file.name for file in files]
        else:
            paths = os.listdir(path)
    
        SetVar(var_, paths)
    
    if module == "search_match":
    
        path = GetParams('path')
        ext_ = GetParams('ext_')
        match = GetParams('match')
        result_ = GetParams('result_')
    
        
        list_ext = []
        
        #files_in_path = os.listdir(path)
        
        
        if ext_:
            target_ext = ext_.lower()
            for file in os.listdir(path):
                if file.lower().endswith(target_ext):
                    list_ext.append(file)
        else:
            list_ext = list_ext = os.listdir(path)
    
        res = []
        if match:
            target_match = match.lower()
            for ele in list_ext:
                if target_match in ele.lower():
                    res.append(ele)
        else:
            res = list_ext
            
        SetVar(result_, res)
    
    if module == "get_metadata":
        def obtener_tamano_en_bytes(ruta_carpeta):
            tamano = os.path.getsize(ruta_carpeta)
            return tamano
        
        def convert_unit(size_in_bytes, unit):
            if unit == "KB":
                return size_in_bytes/1024
            elif unit == "MB":
                return size_in_bytes/(1024*1024)
            elif unit == "GB":
                return size_in_bytes/(1024*1024*1024)
            else:
                return size_in_bytes
        
        path = GetParams('path')
        option = GetParams('option')
        file_name = GetParams('file_name')
        result_ = GetParams('result_')
        option_unit = GetParams('option_unit')
        ext_ = GetParams('ext')
        
        if ext_ == "":
            ext_ = None
        if file_name == "":
            file_name = None
        res = []
        
        if option == "all":        
            if file_name:
                for _file in os.listdir(path):
                    if file_name in _file:
                        path2 = path + "/" + _file
                        modified = dt.datetime.fromtimestamp(os.path.getmtime(path2))
                        date_modified = modified.strftime("%d/%m/%Y, %H:%M")
                        created = dt.datetime.fromtimestamp(os.path.getctime(path2))
                        date_created = created.strftime("%d/%m/%Y, %H:%M")
                        size = obtener_tamano_en_bytes(path2)
                        realSize = convert_unit(size, option_unit)
                        realSize = "%.2f" % round(realSize, 2)
                        res.append({"nombre":f"{_file}", "peso":f"{realSize}  {option_unit}", "modificado":f"{date_modified}", "creado":f"  {date_created}"})
            
            elif ext_:
                for _file in os.listdir(path):
                    if _file.endswith(ext_):
                        path2 = path + "/" + _file
                        modified = dt.datetime.fromtimestamp(os.path.getmtime(path2))
                        created = dt.datetime.fromtimestamp(os.path.getctime(path2))
                        date_modified = modified.strftime("%d/%m/%Y, %H:%M")
                        date_created = created.strftime("%d/%m/%Y, %H:%M")
                        size = obtener_tamano_en_bytes(path2)
                        realSize = convert_unit(size, option_unit)
                        realSize = "%.2f" % round(realSize, 2)
                        res.append({"nombre":f"{_file}", "peso":f"{realSize}  {option_unit}", "modificado":f"{date_modified}", "creado":f"  {date_created}"})
            
            else:
                for _file in os.listdir(path):
                    path2 = path + "/" + _file
                    modified = dt.datetime.fromtimestamp(os.path.getmtime(path2))
                    created = dt.datetime.fromtimestamp(os.path.getctime(path2))
                    date_modified = modified.strftime("%d/%m/%Y, %H:%M")
                    date_created = created.strftime("%d/%m/%Y, %H:%M")
                    size = obtener_tamano_en_bytes(path2)
                    realSize = convert_unit(size, option_unit)
                    realSize = "%.2f" % round(realSize, 2)
                    res.append({"nombre":f"{_file}", "peso":f"{realSize}  {option_unit}", "modificado":f"{date_modified}", "creado":f"  {date_created}"})
             
        elif option == "nameFile":
            if ext_ is not None and file_name is None:
                for _file in os.listdir(path):
                    if _file.endswith(ext_):
                        res.append({"nombre":f"{_file}"})
                        
            elif file_name is not None and ext_ is None:
                for _file in os.listdir(path):
                    if file_name in _file:
                        res.append({"nombre":f"{_file}"})
                        
            elif file_name is None and ext_ is None:
                for _file in os.listdir(path):
                    res.append({"nombre":f"{_file}"})
                        
        elif option == "weight":
            if ext_ is not None and file_name is None:
                for _file in os.listdir(path):
                    if _file.endswith(ext_):
                        path2 = path + "/" + _file
                        size = obtener_tamano_en_bytes(path2)
                        realSize = convert_unit(size, option_unit)
                        realSize = "%.2f" % round(realSize, 2)
                        res.append({"nombre":f"{_file}", "peso":f"{realSize}  {option_unit}"})
            elif file_name is not None and ext_ is None:
                for _file in os.listdir(path):
                    if file_name in _file:
                            path2 = path + "/" + _file
                            size = obtener_tamano_en_bytes(path2)
                            realSize = convert_unit(size, option_unit)
                            realSize = "%.2f" % round(realSize, 2)
                            res.append({"nombre":f"{_file}", "peso":f"{realSize}  {option_unit}"})
                        
            elif file_name is  None and ext_ is None:
                for _file in os.listdir(path):
                    path2 = path + "/" + _file
                    size = obtener_tamano_en_bytes(path2)
                    realSize = convert_unit(size, option_unit)
                    realSize = "%.2f" % round(realSize, 2)
                    res.append({"nombre":f"{_file}", "peso":f"{realSize}  {option_unit}"})
                
        elif option == "date_creation":
            if ext_ is not None and file_name is None:
                for _file in os.listdir(path):
                    if _file.endswith(ext_):
                        created = dt.datetime.fromtimestamp(os.path.getctime(path))
                        date_created = created.strftime("%d/%m/%Y, %H:%M")
                        res.append(_file)
                        res.append({"creado":f"  {date_created}"})
                        
            elif file_name is not None and ext_ is None:
                for _file in os.listdir(path):
                    if file_name in _file:
                        created = dt.datetime.fromtimestamp(os.path.getctime(path))
                        date_created = created.strftime("%d/%m/%Y, %H:%M")
                        res.append(_file)
                        res.append({"creado":f"  {date_created}"})
                        
            elif file_name is  None and ext_ is None:
                for _file in os.listdir(path):
                    created = dt.datetime.fromtimestamp(os.path.getctime(path))
                    date_created = created.strftime("%d/%m/%Y, %H:%M")
                    res.append(_file)
                    res.append({"creado":f"  {date_created}"})
        
        elif option == "date_modification":
            if ext_ is not None and file_name is None:
                for _file in os.listdir(path):
                    if _file.endswith(ext_):
                        modified = dt.datetime.fromtimestamp(os.path.getmtime(path))
                        date_modified = modified.strftime("%d/%m/%Y, %H:%M")
                        res.append(_file)
                        res.append({"modificado":f"  {date_modified}"})
                        
            elif file_name is not None and ext_ is None:
                for _file in os.listdir(path):
                    if file_name in _file:
                        modified = dt.datetime.fromtimestamp(os.path.getmtime(path))
                        date_modified = modified.strftime("%d/%m/%Y, %H:%M")
                        res.append(_file)
                        res.append({"modificado":f"  {date_modified}"})
                        
            elif file_name is None and ext_ is None:
                for _file in os.listdir(path):
                    modified = dt.datetime.fromtimestamp(os.path.getmtime(path))
                    date_modified = modified.strftime("%d/%m/%Y, %H:%M")
                    res.append(_file)
                    res.append({"modificado":f"  {date_modified}"})
                        
        SetVar(result_, res)


    if module == "delete_folder_content":
        path = GetParams('path')
        result = GetParams('result_')
    
        try:
            shutil.rmtree(path)
            os.mkdir(path)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
    
    if module == "copy_folder":
        path = GetParams('path')
        path2 = GetParams('path2')
        result = GetParams('result_')
        try:
            nombre_directorio = os.path.basename(os.path.normpath(path))
            nuevo_destino = os.path.join(path2, nombre_directorio)
            shutil.copytree(path, nuevo_destino, dirs_exist_ok=True, ignore_dangling_symlinks=True)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e

    if module == "copy_content_folder":
        path = GetParams('path')
        path2 = GetParams('path2')
        result = GetParams('result_')
        try:
            shutil.copytree(path, path2, dirs_exist_ok=True, ignore_dangling_symlinks=True)
            SetVar(result, True)
        except Exception as e:
            SetVar(result, False)
            PrintException()
            raise e
        
except Exception as e:
   PrintException()
   raise e
