import sqlite3

class Comunicacion():
    def __init__(self):
        self.conexion = sqlite3.connect('db1.db')
        
    def insterta_datos(self, nombre, descripcion, precio, stock):
            cursor = self.conexion.cursor()
            bd = '''INSERT INTO productos (NOMBRE, DESCRIPCION, PRECIO, STOCK)
            VALUES('{}', '{}', '{}', '{}')'''.format(nombre, descripcion, precio, stock)
            cursor.execute(bd)
            self.conexion.commit()
            cursor.close()
            
    def mostrar_datos(self):
            cursor = self.conexion.cursor()
            bd = "SELECT * FROm productos"
            cursor.execute(bd)
            datos = cursor.fetchall()
            return datos
        
    def elimina_datos(self, id_producto):
        cursor = self.conexion.cursor()
        try:
                query = '''DELETE FROM productos WHERE ID = ?'''
                cursor.execute(query, (id_producto,))
                self.conexion.commit()
        except sqlite3.Error as e:
         print(f"Error al eliminar datos: {e}")
        finally:
                cursor.close()
            
    def actualiza_datos(self, ID, nombre, descripcion, precio, stock):
            cursor = self.conexion.cursor()
            bd = '''UPDATE productos SET NOMBRE = '{}', DESCRIPCION = '{}', PRECIO = '{}', STOCK = '{}' WHERE ID = '{}' '''.format(nombre, descripcion, precio, stock)
            cursor.execute(bd)
            dato = cursor.rowcount
            self.conexion.commit()
            cursor.close()
            return dato
            