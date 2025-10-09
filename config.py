#!/usr/bin/python
from configparser import ConfigParser
from pathlib import Path
import sys
from config_keys import HOST_DATABASE

# Base directory for the project (common folder for all PCs)
if getattr(sys, 'frozen', False):
    # If running as PyInstaller exe
    BASEDIR = Path(sys.executable).parent
else:
    # If running as normal Python script
    BASEDIR = Path(r"\\nas01\DATOS\Comunes\EIPSA-ERP")


# Helper function to build paths
def get_path(*subpaths):
    """
    Returns an absolute path by joining BASEDIR with subfolders/files.

    Example:
        get_path("Resources", "Iconos", "icon.ico")
    """
    return (BASEDIR.joinpath(*subpaths)).resolve()


# Database configuration reader
def config(filename=r"C:\Program Files\ERP EIPSA\database.ini", section='postgresql'):
    """
    Reads database configuration from an INI file and returns the configuration parameters as a dictionary.

    Args:
        filename (str): Path to the INI file containing the database configuration.
        section (str): The section in the INI file to read configuration from. Default is 'postgresql'.

    Returns:
        dict: A dictionary containing the database configuration parameters.

    Raises:
        Exception: If the specified section is not found in the INI file.
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    required_keys = ['database', 'user', 'password']

    for key in required_keys:
        if parser.has_option(section, key):
            db[key] = parser.get(section, key)
        else:
            raise Exception(f"Missing required parameter '{key}' in section '{section}'")

    db['host'] = HOST_DATABASE

    return db