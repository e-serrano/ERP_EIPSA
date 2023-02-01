import tkinter as tk
from tkinter import *
import os, sys
from Window_creation import *

#importación de módulos de SQL
             
class Login:
    def __init__(self):
        #Creating initial window
        self.login_window = Windows()
        self.frame_login=Frame(self.login_window)
        self.frame_login.pack()
        self.frame_login.config(width=650, height=400)
        Label(self.frame_login, text='').pack()

        #User Name input
        Label(self.frame_login, text= 'Nombre de Usuario: ').pack()
        self.namelog = Entry(self.frame_login)
        self.namelog.pack()
        Label(self.frame_login, text='').pack()

        #Password input
        Label(self.frame_login, text= 'Contraseña: ').pack()
        self.passwordlog = Entry(self.frame_login, show='*')
        self.passwordlog.pack()
        Label(self.frame_login, text='').pack()

        #Entry Button
        Button(self.frame_login, text='Acceder', command = self.verification_login).pack()

        self.login_window.mainloop()

    def verification_login(self):
        window = self.login_window
        name = self.namelog.get()
        password = self.passwordlog.get()
        list_files = os.listdir(os.getcwd() + '\Passwords')
        if name in list_files:
            verif_file = open(name, 'r')
            verification = verif_file.read().splitlines()
            if password in verification:
                print('Abrir aplicación')
            else:
                self.password_error()
        else:
            self.user_error()

        del self.login_window,self.frame_login, self.namelog, self.passwordlog, window, name, password, list_files, verif_file, verification

    def password_error(self):
        self.pass_error_root = Toplevel()
        Label(self.pass_error_root, text = 'Contraseña incorrecta').pack()
        Button(self.pass_error_root, text = 'Ok', command = self.pass_error_root.destroy).pack()
        self.pass_error_root.mainloop()

        del self.pass_error_root

    def user_error(self):
        self.user_error_root=Toplevel()
        Label(self.user_error_root, text = 'Usuario incorrecto o inexistente').pack()
        Button(self.user_error_root, text ='Ok', command = self.user_error_root.destroy).pack()
        self.user_error_root.mainloop()

        del self.user_error_root

if __name__ == '__main__':
    application = Login()
    application.mainloop()