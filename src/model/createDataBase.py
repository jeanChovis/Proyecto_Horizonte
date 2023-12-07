from src.model.declarative_base import Session, engine, Base
from src.model.employer import Employer
from src.model.work import Work
from src.model.voucher import Voucher
from src.model.employee import Employee
from src.model.company_data import CompanyData
from src.model.discount import Discount
from src.model.remuneration import Remuneration
from datetime import date


if __name__ == '__main__':

    Base.metadata.create_all(engine)
    session = Session()

    # VALORES POR DEFECTO DE LA APLICACION

    # Crear dato de la empresa
    datoEmpresa = CompanyData(rucCo='20136150473', businnesnameCo='Consorcio Minero', categoryCo='Minera',
                              addresCo='Jirón García Naranjo 1176, Lima 15018')
    session.add(datoEmpresa)

    # Crear datos del Empleador
    adminCompany = Employer(dniEmpl = '42462829', nameEmpl='Julio', surnameDadEmpl='Cesar', surnameMomEmpl='Aldecoa',
                            emailEmpl='jcesar@cmh.com.pe', phoneEmpl=981279659)
    session.add(adminCompany)

    # Crear remuneracion
    remuneration1 = Remuneration(bonusOvertime=30.00, bonusMobility=300.00, bonusSupplemt=100.00, computableRemun=150.00,
                                 cts=250.00, totalRemun=1000.00)
    remuneration2 = Remuneration(bonusOvertime=20.00, bonusMobility=200.00, bonusSupplemt=200.00, computableRemun=2500.00,
                                 cts=350.00, totalRemun=500.00)
    session.add(remuneration1)
    session.add(remuneration2)

    # Crear Descuentos
    discount1 = Discount(lackDisc=10.00, lateDisc=5.00, totalDisc=15.00)
    discount2 = Discount(lackDisc=20.00, lateDisc=1.00, totalDisc=21.00)
    session.add(discount1)
    session.add(discount2)

    # Crear Work
    work1 = Work(daysWk=20, extraHours=3, daysNoWk=10, minutesNoWk=50, netIncome=500.00, remuneration=remuneration1, discounts=discount1)
    work2 = Work(daysWk=30, extraHours=2, daysNoWk=15, minutesNoWk=40, netIncome=400.00, remuneration=remuneration2, discounts=discount2)
    session.add(work1)
    session.add(work2)

    # Crear empleados temp
    empleado1 = Employee(dniEmp='76266001', nameEmp='Jose', surnameDadEmp='Perez', surnameMomEmp='Echevarria',
                         emailEmp='jperez@cmh.com.pe', phoneEmp=999666333, savAcctEmp=9876543219,
                         minWageEmp=200.00, work=work1)
    empleado2 = Employee(dniEmp='77785421', nameEmp='Maria', surnameDadEmp='Carmen', surnameMomEmp='Pariona',
                         emailEmp='mcarmen@cmh.com.pe', phoneEmp=985698569, savAcctEmp=1234567890,
                         minWageEmp=300.00, work=work2)
    session.add(empleado1)
    session.add(empleado2)

    # Crear Voucher
    voucher1 = Voucher(dateVch=date(2023, 10, 10), employer=adminCompany, companyData=datoEmpresa,
                       employee=empleado1)
    voucher2 = Voucher(dateVch=date(2022, 11, 11), employer=adminCompany, companyData=datoEmpresa,
                       employee=empleado2)
    session.add(voucher1)
    session.add(voucher2)

    session.commit()
    session.close()
