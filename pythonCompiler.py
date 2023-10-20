#!/usr/pin/python


# start import

import os
import sys
import subprocess
import tempfile

# end import


# start variables

version = "1.0.1"

# end variables


# start functions

def help():
    print("PythonCompiler v" + version)
    print("Usage: pythonCompiler <python file> [output path]\n")
    print("This programm calls the \"pyinstaller\" programm form python and converts a .py file to a .exe file.\n")
    print("Dependency:\nYou have to install pyinstaller.\nOpen cmd and use \"pip install pyinstaller\" to install it\n\n\n")
    input("Press Enter to exit")
    return 0

# ----------

def getPyInstallerExe():
    current_user = os.getlogin()

    base_path = os.path.join("c:\\", "users", current_user, "appdata", "local", "packages")

    if not os.path.exists(base_path):
        print("Base path does not exist")
        return 1

    path_pyinstaller_exes = []

    for i in os.listdir(base_path):
        if "PythonSoftwareFoundation.Python.3." in i:
            python_version = "Python" + i.split("_")[0].split(".", maxsplit = 2)[2].replace(".", "")
            path_pyinstaller_exes.append(os.path.join(base_path, i, "localcache", "local-packages", python_version, "scripts", "pyinstaller.exe"))
    for path_pyinstaller_exe in path_pyinstaller_exes:
        if os.path.exists(path_pyinstaller_exe):
            return path_pyinstaller_exe
    
    print("Pyinstaller path does not exist")
    help()
    return 1

# ----------

def compilePython(source_path, path_destination):

    if not os.path.exists(source_path):
        print("ERROR: \"" + source_path + "\" does not exist")
        return 1


    path_pyinstaller_exe = getPyInstallerExe()
    if not os.path.splitext(path_pyinstaller_exe)[1] == ".exe":
        return 1

    with tempfile.TemporaryDirectory() as temp_dir:
        command = [path_pyinstaller_exe, source_path, "--onefile", "--distpath", path_destination, "--workpath", temp_dir, "--specpath", temp_dir]
        return subprocess.run(command).returncode

# ----------

def main():
    args = sys.argv

    if len(args) == 1:
        return help()
    elif len(args) > 3:
        print("ERROR: Too many arguments")
        return 1
    elif len(args) == 2:
        path_file = args[1]
        path_destination = "."
    else:
        path_file = args[1]
        path_destination = args[2]

    return compilePython(path_file, path_destination)


# end functions


sys.exit(main())