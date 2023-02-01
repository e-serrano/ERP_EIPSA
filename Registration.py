import tkinter as tk
from tkinter import *
import os, sys
from Window_creation import *

class Register:
    # def __init__(self):
    #     self.register_window = Windows()
    #     self.frame_register = Frame(self.register_window)
    #     self.frame_register.pack()

    #     #User Name input
    #     Label(self.frame_register, text= 'Nombre de Usuario: ').pack()
    #     self.namereg = Entry(self.frame_register)
    #     self.namereg.pack()
    #     Label(self.frame_register, text='').pack()

    #     #Password input
    #     Label(self.frame_register, text= 'Contraseña: ').pack()
    #     self.passwordreg = Entry(self.frame_register, show='*')
    #     self.passwordreg.pack()
    #     Label(self.frame_register, text='').pack()

    #     #Entry Button
    #     Button(self.frame_register, text='Registrar', command = self.user_register).pack()

    #     self.register_window.mainloop()

    def user_register(self):
        path=os.path.join(os.getcwd(),'Passwords',self.namereg.get())
        file=open(path, 'w')
        file.write(self.namereg.get() + '\n' + self.passwordreg.get())
        file.close()
        self.reg_root=Toplevel()
        Label(self.reg_root, text = 'Usuario registrado con éxito').pack()
        Button(self.reg_root, text ='Ok', command = self.reg_root.destroy).pack()
        self.register_window.destroy()
        self.reg_root.mainloop()

        del self.register_window, self.frame_register, self.namereg, self.passwordreg, path, file, self.reg_root



if __name__ == '__main__':
    application = Register()