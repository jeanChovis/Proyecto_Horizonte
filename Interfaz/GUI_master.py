from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from tkinter.font import BOLD
import src.GUI.generic as utl
from datetime import datetime
from src.GUI.GUI_voucher import Voucher
from src.model.declarative_base import Session, engine, Base
from src.model.employer import Employer
from src.model.company_data import CompanyData
from src.model.employee import Employee
from src.GUI.GUI_voucher import Voucher
from src.model.work import Work
from src.model.remuneration import Remuneration
from src.model.discount import Discount
from src.GUI.conexion import conexion
import sqlite3
import os
class MasterPanel:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('CONSORCIO MINERO HORIZONTE')
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.config(bg='#fcfcfc')
        self.root.resizable(0, 0)

        # Conexion
        miConexion, miCursor = conexion()

        frame_main = self.interfaz_principal(miCursor, miConexion)

        self.root.mainloop()

    def rellenaCampos(self, idEmpSelec, miCursor):
        miCursor.execute("SELECT * FROM tblEmployee WHERE idEmp = ?", (idEmpSelec,))
        empleado = miCursor.fetchone()
        miCursor.execute("SELECT nameEmp || ' ' || surnameDadEmp || ' ' || surnameMomEmp AS 'NOMBRE COMPLETO' FROM tblEmployee WHERE idEmp = ?", (idEmpSelec,))
        nombreCompletoTemp = miCursor.fetchone()
        nombreCompleto = nombreCompletoTemp[0]

        if empleado:
            _, dni, nombre, apellido_paterno, apellido_materno, email, telefono, cuenta_ahorro, sueldo_basico, _ = empleado
            self.dni_Emp.delete(0, tk.END)
            self.dni_Emp.insert(0, dni)

            self.nombre_Emp.delete(0, tk.END)
            self.nombre_Emp.insert(0, nombreCompleto)

            self.telefono_Emp.delete(0, tk.END)
            self.telefono_Emp.insert(0, telefono)

            self.email_Emp.delete(0, tk.END)
            self.email_Emp.insert(0, email)

            self.cuentaAhorro_Emp.delete(0, tk.END)
            self.cuentaAhorro_Emp.insert(0, cuenta_ahorro)

            self.sueldoB_Emp.delete(0, tk.END)
            self.sueldoB_Emp.insert(0, sueldo_basico)

        else:
            self.dni_Emp.delete(0, tk.END)
            self.nombre_Emp.delete(0, tk.END)
            self.telefono_Emp.delete(0, tk.END)
            self.email_Emp.delete(0, tk.END)
            self.cuentaAhorro_Emp.delete(0, tk.END)
            self.sueldoB_Emp.delete(0, tk.END)

    def rellenar_campos_empleado(self, selected_id, miCursor):
        # Llamar al método rellenaCampos con el ID seleccionado
        self.rellenaCampos(selected_id, miCursor)

    def obtener_valor_radiobutton(self, var):
        valor_seleccionado = var.get()
        return valor_seleccionado

    def obtener_valor_spinbox(self, spinbox):
        valor_seleccionado = spinbox.get()
        return valor_seleccionado

    def obtener_valor_combobox(self, combobox):
        valor_seleccionado = combobox.get()
        return valor_seleccionado

    def cancelaDatos(self, combo, dni, emp, telefono, email, cuentaAh, sueldo, spinbHoraEx, radioBuMovil, spinbDNL, spinbMinT):

        combo.set("Selecciona una opción")
        dni.delete(0, tk.END)
        emp.delete(0, tk.END)
        telefono.delete(0, tk.END)
        email.delete(0, tk.END)
        cuentaAh.delete(0, tk.END)
        sueldo.delete(0, tk.END)
        spinbHoraEx.delete(0, tk.END)
        spinbHoraEx.insert(0, "0")
        radioBuMovil.set("")
        spinbDNL.delete(0, tk.END)
        spinbDNL.insert(0, "0")
        spinbMinT.delete(0, tk.END)
        spinbMinT.insert(0, "0")

    def almacenaDatos(self, select_IDEmp, select_HoraEx, select_Movil, selectDNL, selectMinT, miCursor, miConexion):

        # Recoje los datos seleccionados
        IDEmp = self.obtener_valor_combobox(select_IDEmp)
        HoEx = self.obtener_valor_spinbox(select_HoraEx)
        Mvl = self.obtener_valor_radiobutton(select_Movil)
        DNL = self.obtener_valor_spinbox(selectDNL)
        MinT = self.obtener_valor_spinbox(selectMinT)


        # Almacena en la tabla REMUNERACION
        if Mvl == "Si":
            miCursor.execute("UPDATE tblRemuneration SET bonusMobility = ? WHERE idRemun =?", (1000, IDEmp))
        else:
            miCursor.execute("UPDATE tblRemuneration SET bonusMobility = ? WHERE idRemun =?", (0, IDEmp))

        # Almacena en la tabla WORK
        miCursor.execute("UPDATE tblWork SET daysWk = ? WHERE idWk = ?", (30-int(DNL), IDEmp))
        miCursor.execute("UPDATE tblWork SET extraHours = ? WHERE idWk = ?", (HoEx, IDEmp))
        miCursor.execute("UPDATE tblWork SET daysNoWk = ? WHERE idWk = ?", (DNL, IDEmp))
        miCursor.execute("UPDATE tblWork SET minutesNoWk = ? WHERE idWk = ?", (MinT, IDEmp))

        miConexion.commit()

        # Calculo de Bonificaciones
        miCursor.execute("SELECT minWageEmp FROM tblEmployee WHERE idEmp = ?", (IDEmp,))
        sueldoBasicoTemp = miCursor.fetchone()
        sueldoBasico = sueldoBasicoTemp[0]
        bonificacionSuplementaria = 0.03 * float(sueldoBasico)
        print(bonificacionSuplementaria)

        miCursor.execute("SELECT extraHours FROM tblWork WHERE idWk = ?", (IDEmp,))
        HoraExtraTemp = miCursor.fetchone()
        HoraExtra = HoraExtraTemp[0]
        pagoHoraNormal = float(sueldoBasico) / 30 / 8
        pagoHoraExtra = 1.5 * float(HoraExtra) * pagoHoraNormal
        print(pagoHoraExtra)

        miCursor.execute("SELECT bonusMobility FROM tblRemuneration WHERE idRemun = ?", (IDEmp,))
        movilidadTemp = miCursor.fetchone()
        movilidad = movilidadTemp[0]
        bonificacionGen = movilidad + bonificacionSuplementaria + pagoHoraExtra
        remuneracionComputable = float(sueldoBasico) + movilidad + bonificacionSuplementaria
        remuneracionTotal = bonificacionGen + 0 # 0 HACE REFERENCIA AL CTS
        print(bonificacionGen)
        print(remuneracionComputable)

        # Rellena tblRemun con calculos Bonificacion
        miCursor.execute("UPDATE tblRemuneration SET bonusOvertime = ? WHERE idRemun = ?", (pagoHoraExtra, IDEmp))
        miCursor.execute("UPDATE tblRemuneration SET bonusSupplemt = ? WHERE idRemun = ?", (bonificacionSuplementaria, IDEmp))
        miCursor.execute("UPDATE tblRemuneration SET computableRemun = ? WHERE idRemun = ?", (remuneracionComputable, IDEmp))
        miCursor.execute("UPDATE tblRemuneration SET cts = ? WHERE idRemun = ?", (0, IDEmp)) # AÑADIR CONDICIONAL PARA EL MES DE MAYO Y NOVIEMBRE
        miCursor.execute("UPDATE tblRemuneration SET totalRemun = ? WHERE idRemun = ?", (remuneracionTotal, IDEmp))


        # Calculo de Descuento
        descuentoFalta = remuneracionComputable/30 * int(DNL)
        descuentoTardanza = remuneracionComputable/30/8/60 * int(MinT)
        descuentoTotal = descuentoTardanza+ descuentoFalta

        # Rellena tblDiscount con calculos Descuento
        miCursor.execute("UPDATE tblDiscount SET lackDisc = ? WHERE idDisc = ?", (descuentoFalta, IDEmp))
        miCursor.execute("UPDATE tblDiscount SET lateDisc = ? WHERE idDisc = ?", (descuentoTardanza, IDEmp))
        miCursor.execute("UPDATE tblDiscount SET totalDisc = ? WHERE idDisc = ?", (descuentoTotal, IDEmp))

        # Rellena tblWork con calculos
        sueldoNeto = float(sueldoBasico) + remuneracionTotal - descuentoTotal
        miCursor.execute("UPDATE tblWork SET netIncome = ? WHERE idWk = ?", (sueldoNeto, IDEmp))

        # Rellena Voucher
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        miCursor.execute("UPDATE tblVoucher SET dateVch = ? WHERE idVch = ?", (fecha_actual, IDEmp))

        miConexion.commit()

        # MUESTRA EL VOUCHER
        #self.root.destroy()
        #Voucher()
        ventana = Voucher(self.root)
    #def abrir_ventana_secundaria(self):
     #   ventana = Voucher(self.root)

    def interfaz_principal(self, miCursor, miConexion):

        # Limpia Pantalla
        for widget in self.root.winfo_children():
            widget.destroy()

        self.Menu_Bar(self.root, miCursor, miConexion)

        self.ruta_actual = os.path.dirname(os.path.realpath(__file__))
        self.ruta_logo = os.path.join(self.ruta_actual, '..', 'images', 'encabezadoMaster.jpg')
        self.logo = utl.Read_Image(self.ruta_logo, (600, 200))
        self.label = tk.Label(self.root, image=self.logo, bg='#bababa')
        self.label.place(x=0, y=0, relwidth=1, relheight=0.3)

        frame_height = int(self.root.winfo_screenheight() * 0.7)
        frame_main = tk.Frame(self.root, bg='#bababa')
        frame_main.place(x=0, y=int(self.root.winfo_screenheight() * 0.3), relwidth=1, relheight=0.8)
        # IDEmpleado
        label_idEmployee = tk.Label(frame_main, text="ID Empleado :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_idEmployee.pack(padx=100, pady=70, anchor=tk.W)

        # ID EMPLEADO
        miCursor.execute("SELECT idEmp FROM tblEmployee")
        ids = miCursor.fetchall()
        opciones_ids = [int(idEmp[0]) for idEmp in ids]
        combo = ttk.Combobox(frame_main, values=opciones_ids, state="readonly")
        combo.place(x=100, y=100)
        combo.set("Selecciona una opción")
        combo.bind("<<ComboboxSelected>>", lambda event: self.rellenar_campos_empleado(combo.get(), miCursor))

        # DNI Empleado
        label_dni_Emp = tk.Label(frame_main, text="DNI :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_dni_Emp.place(x=300, y=70)
        self.dni_Emp = ttk.Entry(frame_main, font=('Times', 14))
        self.dni_Emp.place(x=300, y=100)


        # Nombre Empleado
        label_nombre_Emp = tk.Label(frame_main, text="Empleado :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_nombre_Emp.place(x=550, y=70)
        self.nombre_Emp = ttk.Entry(frame_main, font=('Times', 14))
        self.nombre_Emp.place(x=550, y=100)

        # Telefono Empleado
        label_telefono_Emp = tk.Label(frame_main, text="Telefono :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_telefono_Emp.place(x=1050, y=70)
        self.telefono_Emp = ttk.Entry(frame_main, font=('Times', 14))
        self.telefono_Emp.place(x=1050, y=100)

        # Email Empleado
        label_email_Emp = tk.Label(frame_main, text="Email :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_email_Emp.place(x=100, y=150)
        self.email_Emp = ttk.Entry(frame_main, font=('Times', 14))
        self.email_Emp.place(x=100, y=180)

        # Cuenta Ahorro Empleado
        label_cuentaAhorro_Emp = tk.Label(frame_main, text="Cuenta Ahorro :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_cuentaAhorro_Emp.place(x=550, y=150)
        self.cuentaAhorro_Emp = ttk.Entry(frame_main, font=('Times', 14))
        self.cuentaAhorro_Emp.place(x=550, y=180)

        # Suedo Basico Empleado
        label_sueldoB_Emp = tk.Label(frame_main, text="Sueldo Basico :", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_sueldoB_Emp.place(x=1000, y=150)
        self.sueldoB_Emp = ttk.Entry(frame_main, font=('Times', 14))
        self.sueldoB_Emp.place(x=1000, y=180)

        # Separacion
        linea = tk.Canvas(frame_main, width=1335, height=2, bg="blue")
        linea.place(x=10, y=220)

        # Remuneracion
        label_Remun = tk.Label(frame_main, text="REMUNERACION", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_Remun.place(x=330, y=230)

        label_HoraEx_Emp = tk.Label(frame_main, text="Horas Extra :", font=('Times', 12), fg="#7d3025", bg='#bababa')
        label_HoraEx_Emp.place(x=150, y=290)
        self.spinbox_HoraEx = tk.Spinbox(frame_main, from_=0, to=23, width=5)
        self.spinbox_HoraEx.place(x=250, y=320)

        label_Movilidad_Emp = tk.Label(frame_main, text="Movilidad :", font=('Times', 12), fg="#7d3025", bg='#bababa')
        label_Movilidad_Emp.place(x=150, y=360)

        self.var = tk.StringVar()
        radio_si = tk.Radiobutton(frame_main, text="Si", variable=self.var, value="Si", fg="#7d3025", bg='#bababa')
        radio_si.place(x=180, y=380)
        radio_no = tk.Radiobutton(frame_main, text="No", variable=self.var, value="No", fg="#7d3025", bg='#bababa')
        radio_no.place(x=180, y=400)


        # Descuento
        label_Desc = tk.Label(frame_main, text="DESCUENTO", font=('Times', 14), fg="#7d3025", bg='#bababa')
        label_Desc.place(x=900, y=230)

        label_Desc = tk.Label(frame_main, text="Dias NO Laborado :", font=('Times', 12), fg="#7d3025", bg='#bababa')
        label_Desc.place(x=700, y=300)
        self.spinbox_DiasNoLab = tk.Spinbox(frame_main, from_=0, to=30, width=5)
        self.spinbox_DiasNoLab.place(x=880, y=300)

        label_Desc = tk.Label(frame_main, text="Minutos Tardanza", font=('Times', 12), fg="#7d3025", bg='#bababa')
        label_Desc.place(x=700, y=340)
        self.spinbox_MinTrd = tk.Spinbox(frame_main, from_=0, to=1440, width=5)
        self.spinbox_MinTrd.place(x=880, y=340)


        boton_CancelCalculo = tk.Button(frame_main, text="CANCELAR", command=lambda: self.cancelaDatos(combo, self.dni_Emp, self.nombre_Emp, self.telefono_Emp, self.email_Emp, self.cuentaAhorro_Emp, self.sueldoB_Emp, self.spinbox_HoraEx, self.var, self.spinbox_DiasNoLab, self.spinbox_MinTrd))
        boton_CancelCalculo.place(x=800, y=450)

        boton_RegistrarCalculo = tk.Button(frame_main, text="GUARDAR", command=lambda: self.almacenaDatos(combo, self.spinbox_HoraEx, self.var, self.spinbox_DiasNoLab, self.spinbox_MinTrd, miCursor, miConexion))
        boton_RegistrarCalculo.place(x=1000, y=450)

        #self.btn_abrir = tk.Button(frame_main, text="Abrir Ventana Secundaria", command=self.abrir_ventana_secundaria)
        #self.btn_abrir.pack(pady=20)

        return frame_main

    def limpiarDatosNE(self, dniNE, nombNE, apPatNE, apMatNE, emailNE, telNE, cuentaNE, sueldoNE):
        #print(self.dni_NE)
        dniNE.delete(0, tk.END)
        nombNE.delete(0, tk.END)
        apPatNE.delete(0, tk.END)
        apMatNE.delete(0, tk.END)
        emailNE.delete(0, tk.END)
        telNE.delete(0, tk.END)
        cuentaNE.delete(0, tk.END)
        sueldoNE.delete(0, tk.END)

    def almacenaDatosNE(self, miCursor, miConexion):
        dniNE = self.dni_NE.get()
        nombreNE = self.nombre_NE.get()
        apPatNE = self.apPat_NE.get()
        apMatNE = self.apMat_NE.get()
        emailNE = self.email_NE.get()
        telfNE = self.tel_NE.get()
        cuentaNE = self.cuenta_NE.get()
        sueldoNE = self.sueldo_NE.get()

        miCursor.execute("INSERT INTO tblEmployee (dniEmp, nameEmp, surnameDadEmp, surnameMomEmp, emailEmp, phoneEmp, "
                         "savAcctEmp, minWageEmp) VALUES (?,?,?,?,?,?,?,?)", (dniNE, nombreNE, apPatNE, apMatNE,
                                                                              emailNE, telfNE, cuentaNE, sueldoNE))
        miConexion.commit()
        valoridWk = miCursor.lastrowid
        miCursor.execute("UPDATE tblEmployee SET idWk = ? WHERE idEmp = ?", (valoridWk, valoridWk))
        miCursor.execute("INSERT INTO tblWork (daysWk, extraHours, daysNoWk, minutesNoWk, netIncome, idRemun, idDisc) VALUES (?,?,?,?,?,?,?)", (0, 0, 0, 0, 0, valoridWk, valoridWk))
        miCursor.execute("INSERT INTO tblRemuneration (bonusOvertime, bonusMobility, bonusSupplemt, computableRemun, cts, totalRemun) VALUES (?,?,?,?,?,?)", (0, 0, 0, 0, 0, 0))
        miCursor.execute("INSERT INTO tblDiscount (lackDisc, lateDisc, totalDisc) VALUES (?,?,?)", (0, 0, 0))
        miConexion.commit()
        messagebox.showinfo(message="Los datos del nuevo empleado se registradon exitosamente !", title="DATOS GUARDADOS")

        self.limpiarDatosNE(self.dni_NE, self.nombre_NE, self.apPat_NE, self.apMat_NE, self.email_NE, self.tel_NE,
                            self.cuenta_NE, self.sueldo_NE)


    def pantalla_NuevoEmp(self, miCursor, miConexion):
        # Limpia Pantalla
        for widget in self.root.winfo_children():
            widget.destroy()

        self.Menu_Bar(self.root, miCursor, miConexion)

        frame_NuevEmp = tk.Frame(self.root, bg='#bcbcbc')
        frame_NuevEmp.place(x=0, y=int(self.root.winfo_screenheight() * 0), relwidth=1, relheight=1)

        label_TitlNuevEmp = tk.Label(frame_NuevEmp, text="NUEVO EMPLEADO", font=('Times', 20, 'bold'), fg="#7d3025", bg='#bababa')
        label_TitlNuevEmp.place(x=580, y=80)

        # DNI
        label_DniNE = tk.Label(frame_NuevEmp, text="DNI :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_DniNE.place(x=400, y=180)
        self.dni_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.dni_NE.place(x=700, y=180)

        # Nombres
        label_nombreNE = tk.Label(frame_NuevEmp, text="NOMBRES :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_nombreNE.place(x=400, y=240)
        self.nombre_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.nombre_NE.place(x=700, y=240)

        # Apellido Paterno
        label_apPNE = tk.Label(frame_NuevEmp, text="APELLIDO PATERNO :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_apPNE.place(x=400, y=300)
        self.apPat_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.apPat_NE.place(x=700, y=300)

        # Apellido Materno
        label_apMNE = tk.Label(frame_NuevEmp, text="APELLIDO MATERNO :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_apMNE.place(x=400, y=360)
        self.apMat_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.apMat_NE.place(x=700, y=360)

        # Email
        label_emailNE = tk.Label(frame_NuevEmp, text="EMAIL :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_emailNE.place(x=400, y=420)
        self.email_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.email_NE.place(x=700, y=420)

        # Telefono
        label_telNE = tk.Label(frame_NuevEmp, text="TELEFONO :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_telNE.place(x=400, y=480)
        self.tel_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.tel_NE.place(x=700, y=480)

        # Cuenta Ahorro
        label_cuentaNE = tk.Label(frame_NuevEmp, text="CUENTA AHORRO :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_cuentaNE.place(x=400, y=540)
        self.cuenta_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.cuenta_NE.place(x=700, y=540)

        # Sueldo Basico
        label_sueldoNE = tk.Label(frame_NuevEmp, text="SUELDO BASICO :", font=('Times', 16), fg="#7d3025", bg='#bababa')
        label_sueldoNE.place(x=400, y=600)
        self.sueldo_NE = ttk.Entry(frame_NuevEmp, font=('Times', 14))
        self.sueldo_NE.place(x=700, y=600)


        boton_CancelNE = tk.Button(frame_NuevEmp, text="CANCELAR",command=lambda: self.limpiarDatosNE(self.dni_NE, self.nombre_NE,
                                                                                                      self.apPat_NE, self.apMat_NE,
                                                                                                      self.email_NE, self.tel_NE,
                                                                                                      self.cuenta_NE, self.sueldo_NE))
        boton_CancelNE.place(x=500, y=670)

        boton_AlmacenaNE = tk.Button(frame_NuevEmp, text="GUARDAR", command=lambda: self.almacenaDatosNE(miCursor, miConexion))
        boton_AlmacenaNE.place(x=600, y=670)

    def Menu_Bar(self, root, miCursor, miConexion):
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

        menu_inicio = tk.Menu(menu_bar, tearoff=0)

        menu_bar.add_cascade(label='Inicio', menu = menu_inicio)

        menu_inicio.add_command(label='Nuevo Empleado', command=lambda: self.pantalla_NuevoEmp(miCursor, miConexion))
        menu_inicio.add_command(label='Calcular Sueldo', command=lambda: self.interfaz_principal(miCursor, miConexion))
        menu_inicio.add_command(label='Salir', command = root.destroy)

        menu_bar.add_cascade(label='Ver')
        menu_bar.add_cascade(label='Ayuda')

