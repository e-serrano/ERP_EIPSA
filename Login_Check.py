import tkinter as tk
from tkinter import *

import os, sys

#importación de módulos de SQL

class Login():
    def __init__(self):
        super().__init__()

    def password_error(self):
        self.pass_error_root = tk.Tk()
        self.pass_error_root.geometry('300x50')
        self.pass_error_root.title('Error')
        self.pass_error_root.iconbitmap('//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico')
        Label(self.pass_error_root, text = 'Contraseña incorrecta').pack()
        Button(self.pass_error_root, text = 'Ok', command = self.pass_error_root.destroy).pack()
        self.pass_error_root.mainloop()

        del self.pass_error_root

    def user_error(self):
        self.user_error_root=tk.Tk()
        self.user_error_root.geometry('300x50')
        self.user_error_root.title('Error')
        self.user_error_root.iconbitmap('//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico')
        Label(self.user_error_root, text = 'Usuario incorrecto o inexistente').pack()
        Button(self.user_error_root, text ='Ok', command = self.user_error_root.destroy).pack()
        self.user_error_root.mainloop()

        del self.user_error_root

if __name__ == '__main__':
    application_login = Login()
    application_login.password_error()