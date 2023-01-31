from tkinter import ttk
from tkinter import *

#importación de módulos de SQL

class Login:
    def __init__(self,window):
        #Creating initial window
        self.window = window
        self.window.title('ERP EIPSA')
        self.window.geometry('300x250')
        Label(self.window, text='').pack()

        #Name input
        Label(self.window, text= 'Nombre: ').pack()
        self.namelog = Entry(self.window)
        self.namelog.pack()
        Label(self.window, text='').pack()

        #Password input
        Label(self.window, text= 'Contraseña: ').pack()
        self.passwordlog = Entry(self.window, show='*')
        self.passwordlog.pack()
        Label(self.window, text='').pack()

        #Entry Button
        ttk.Button(self.window, text='Acceder', command=self.verification_login).pack()

    def verification_login(self):
        print(self.namelog.get())

if __name__ == '__main__':
    window=Tk()
    application = Login(window)
    window.mainloop()