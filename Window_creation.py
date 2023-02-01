import tkinter as tk
from tkinter import *
import os, sys

class Windows(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('ERP EIPSA')
        self.iconbitmap('eipsa.ico')
        self.geometry('650x400')