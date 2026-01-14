import sys
import os
from pathlib import Path

# imports dummy
import PySide6
import psutil
import psycopg2
import tkinter
import datetime
import matplotlib
import io
import email
import time
import shutil
import PyPDF2
import random
import copy
import locale
import smtplib
import config
import configparser
import re
import math
import traceback
import pathlib
import docxtpl
import fnmatch
import hashlib
import string
import openpyxl
import base64
import pypdf
import win32api
from PIL import Image
import fpdf
import tkinter.filedialog

import utils
import windows
import config
import runpy

import importlib.util

# ----------------------------
# Select functions directory
# ----------------------------
def get_functions_dir():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "01 FUNCIONES")
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "01 FUNCIONES")

def import_all_py(folder, package_prefix=""):
    """
    Importa todos los .py de la carpeta y subcarpetas dinámicamente,
    registrándolos en sys.modules.
    """
    for root, dirs, files in os.walk(folder):
        # Convert relative path to package name
        rel_path = os.path.relpath(root, folder)
        if rel_path == ".":
            rel_package = package_prefix
        else:
            rel_package = package_prefix + "." + ".".join(rel_path.replace("\\", "/").split("/"))
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(root, file)
                module_name = (rel_package + "." + file[:-3]).strip(".")

                # Delete cache if exists
                if module_name in sys.modules:
                    del sys.modules[module_name]

                # Load module from disk
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                sys.modules[module_name] = module

# ---------------------
# MAIN
# ---------------------

FUNCTIONS_DIR = get_functions_dir()
if FUNCTIONS_DIR not in sys.path:
    sys.path.insert(0, FUNCTIONS_DIR)

try:
    # 1️⃣ Import .py files dynamically
    import_all_py(os.path.join(FUNCTIONS_DIR, "windows"), package_prefix="windows")
    import_all_py(os.path.join(FUNCTIONS_DIR, "utils"), package_prefix="utils")
    import_all_py(os.path.join(FUNCTIONS_DIR, "config"), package_prefix="config")

    # 2️⃣ Execute Main_Window
    from windows.Main_Window import start_app
    start_app()

except Exception:
    print("ERROR al cargar la app:")
    traceback.print_exc()
    # input("Pulsa Enter para salir...")
    # sys.exit(1)
