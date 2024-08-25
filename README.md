<h1 align="center"> ERP EIPSA </h1>

<p align="center">
<img src="https://img.shields.io/badge/STATUS-IN%20DEVELOPMENT-green">
</p>
   
This application is a Windows desktop application for a particular industrial company. Based on an ERP (Enterprise Resource Planning) system to manage the different daily activities of the different sections of the company. These sections are differentiated thanks to a role system for users, where each role has its own functionalities.

## Index
* [Description](#description)
* [Prerequisites](#prerequisites-)
* [Deployment 📦](#deployment-)
* [Built With 🛠️](#built-with-%EF%B8%8F)

## Description
This application allows the unification and organization of all areas, that is, to be a system that allows the traceability of all processes and, therefore, leads to the planning and optimization of resources. 
<br><br>
Data is storaged in a database hosted on a local server. This database is managed with PostgreSQL. The database diagram can be seen in the following pdf: 
[Database Diagram](https://github.com/user-attachments/files/16575592/ESQUEMA.BASE.DE.DATOS.pdf)
<br><br>
Since the user system is role-based, each user has access to a specific part of the application, which means that they only have access to certain functionalities specific to their position. A diagram of the application for each type of role can be seen here:
[Application diagram](https://miro.com/app/board/uXjVKtByFCY=/?share_link_id=989377658782)

## Prerequisites 📋
The user must have access to the local server where the database is hosted. In addition, he/she must also have administrator permissions or contact the system administrator to handle the internal installation of the application.
For more details of such installation, please read the following document: 
[Setup Manual](https://github.com/e-serrano/ERP_EIPSA/blob/main/Manuals/Manual%20Instalaci%C3%B3n.pdf)

## Deployment 📦
To create the exe file, the following command should be run on command prompt. All .py files must be in the same path and the command console must be executed in the same path.
```
pyinstaller --windowed --onefile --icon=icon.ico EIPSA-ERP.py
```
Options used:
* --windowed: Do not provide a console window for standard i/o
* --onefile: Create a one-file bundled executable.
* --icon: Apply the icon to a Windows executable. Icon should be .ico format

## Built With 🛠️
![Python](https://img.shields.io/badge/python-14354C?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)

### Libraries
* PyQt6: For the application interface.
* Tkinter: For popup messages or dialog boxes.
* Pandas: For data management and results display.
* Psycopg2: For database connection and queries.  
* Matplotlib: For graph generation.
* Configparser: For reading the .ini file created during the installation process.
* locale: For setting the regional configuration.
* os: For operating system dependent functionalities.
* re: For regular expressions matching operations.
* datetime: For date and time manipulation.
* hashlib: For password encryption.
* openpyxl: For Excel file creation and modification.
* docxtpl: For Word file creation and modification.
* PyFPDF: For creation and modification of PDF files.
* smtplib: For sending mails.
* win32api: For Windows processes manipulation.
* psutil: For information retrieval and process manipulation.
* pyinstaller: For creating .exe file


  
  
  
  
