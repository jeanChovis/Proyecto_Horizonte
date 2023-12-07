import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import src.GUI.generic as utl
from .GUI_master import MasterPanel
from src.GUI.conexion import conexion
import os

class App:

    def verify(self):
        #miConexion, miCursor = conexion()
        #miCursor.execute("SELECT emailEmpl FROM tblEmployer") # ESTO JALA TODA LA COLUMNA EMAIL
        #usuarioTemp = miCursor.fetchone()


        usr = self.user.get()
        psw = self.password.get()
        if(usr == "root" and psw == "12345"):
            self.root.destroy()
            MasterPanel()
        else:
            messagebox.showerror(message="Datos incorrectos", title="Mensaje")

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('CONSORCIO MINERO HORIZONTE')
        self.root.geometry('650x400')
        self.root.config(bg='#fcfcfc')
        self.root.resizable(0,0)
        utl.Center_Window(self.root,650,400)

        ruta_actual = os.path.dirname(os.path.realpath(__file__))
        ruta_logo = os.path.join(ruta_actual, '..', 'images', 'logo.jpg')

        logo = utl.Read_Image(ruta_logo, (200, 200))

        # Frame logo
        frame_logo = tk.Frame(self.root, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#3a7ff6')
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#3a7ff6')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame form
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # Frame Form Top
        frame_form_top = tk.Frame(frame_form, height=40, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de Sesion", font=('Times', 30), fg="#666a88", bg='#fcfcfc', pady=40)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Frame Form Fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Fill User
        label_user = tk.Label(frame_form_fill, text="Usuario", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        label_user.pack(fill=tk.X, padx=20, pady=5)
        self.user = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.user.pack(fill=tk.X, padx=20, pady=10)

        # Fill Password
        label_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        label_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        # Button Login
        login = tk.Button(frame_form_fill, text="LOG IN", font=('Times', 15, BOLD), bg='#3a7ff6', bd=0, fg="#fff", command=self.verify)
        login.pack(fill=tk.X, padx=20, pady=10)

        #login.bind("<Return>", (lambda event: self.verify()))

        self.root.mainloop()
