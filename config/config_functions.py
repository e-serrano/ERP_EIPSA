#!/usr/bin/python
from configparser import ConfigParser
from pathlib import Path
from config.config_keys import HOST_DATABASE, NAME_DATABASE, INI_FILE_PATH, APP_PATH


# Helper function to build paths
def get_path(*subpaths):
    """
    Returns an absolute path by joining APP_PATH with subfolders/files.

    Example:
        get_path("Resources", "Iconos", "icon.ico")
    """
    return APP_PATH.joinpath(*subpaths)


# Database configuration reader
def config_database(section='postgresql'):
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
    if INI_FILE_PATH.exists():
        ini_file = INI_FILE_PATH
    else:
        ini_file = Path(r"C:\Program Files\ERP EIPSA\database.ini")

    parser.read(ini_file)

    # get section, default to postgresql
    db = {}
    required_keys = ['user', 'password']

    for key in required_keys:
        if parser.has_option(section, key):
            db[key] = parser.get(section, key)
        else:
            raise Exception(f"Missing required parameter '{key}' in section '{section}'")

    db['host'] = HOST_DATABASE
    db['database'] = NAME_DATABASE

    return db


def config_sql_engine():
    """
    Creates and returns a SQLAlchemy engine using the database configuration.

    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy engine instance.
    """
    from sqlalchemy import create_engine

    database_params = config_database()
    sql_engine = create_engine(f"postgresql+psycopg2://{database_params['user']}:{database_params['password']}@{HOST_DATABASE}/{NAME_DATABASE}")
    return sql_engine