from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from src.GUI.generic import Center_Window
from tkinter.font import BOLD
import src.GUI.generic as utl
from datetime import datetime
from src.GUI.conexion import conexion
import sqlite3
import os


class Voucher:
    def __init__(self, root):
        self.root = tk.Tk()
        self.root.title('VOUCHER')
        aplicationWidth = 600
        aplicationHeight = 500
        Center_Window(self.root, aplicationWidth, aplicationHeight)
        self.root.config(bg='#fcfcfc')
        self.root.resizable(0, 0)



        self.btn_cerrar = tk.Button(self.root, text="Cerrar Ventana", command=self.cerrar_ventana)
        self.btn_cerrar.pack(pady=20)

    def cerrar_ventana(self):
        self.root.destroy()



        '''
        self.voucher = tk.Tk()
        self.voucher.title('VOUCHER')
        aplicationWidth = 600
        aplicationHeight = 500
        Center_Window(self.voucher, aplicationWidth, aplicationHeight)
        self.voucher.config(bg='#fcfcfc')
        self.voucher.resizable(0, 0)

        label_dni_Emp = tk.Label(self.voucher, text="DNI :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_dni_Emp.place(x=300, y=70)


        self.voucher.mainloop()
        '''