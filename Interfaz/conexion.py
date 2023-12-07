import sqlite3
def conexion():
    try:
        miConexion = sqlite3.connect("E:\\Horizonte_Proyect\\HorizonteProgram\\src\\model\\DBHorizonte.sqlite")
        miCursor = miConexion.cursor()
        return miConexion, miCursor
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None, None

