#!/usr/bin/python
from configparser import ConfigParser


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
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    # print(db)
    return db