from tkinter import Tk, Button, Entry, Label, Scrollbar, Frame, messagebox, ttk
from tkinter import StringVar
from conexion_sql import Comunicacion
from time import strftime
import pandas as pd

class Ventana(Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.nombre = StringVar()
        self.descripcion = StringVar()
        self.precio = StringVar()
        self.stock = StringVar()
        
        self.base_datos = Comunicacion()
        self.widgets()
        
    def widgets(self):
        # Frame forms
        self.frame_uno = Frame(self.master, bg='white', height=200, width=800)
        self.frame_uno.grid(column=0, row=0, sticky='nsew')
        # Frame table
        self.frame_dos = Frame(self.master, bg='white', height=300, width=800)
        self.frame_dos.grid(column=0, row=1, sticky='nsew')
        
        self.frame_uno.columnconfigure([0, 1, 2], weight=1)
        self.frame_uno.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.frame_dos.columnconfigure(0, weight=1)
        self.frame_dos.rowconfigure(0, weight=1)

        #Labels del form
        Label(self.frame_uno, text='Nombre:', bg='white').grid(column=0, row=0, sticky='e', padx=5, pady=5)
        Entry(self.frame_uno, textvariable=self.nombre, width=25).grid(column=1, row=0, padx=5, pady=5)

        Label(self.frame_uno, text='Descripción:', bg='white').grid(column=0, row=1, sticky='e', padx=5, pady=5)
        Entry(self.frame_uno, textvariable=self.descripcion, width=25).grid(column=1, row=1, padx=5, pady=5)

        Label(self.frame_uno, text='Precio:', bg='white').grid(column=0, row=2, sticky='e', padx=5, pady=5)
        Entry(self.frame_uno, textvariable=self.precio, width=25).grid(column=1, row=2, padx=5, pady=5)

        Label(self.frame_uno, text='Stock:', bg='white').grid(column=0, row=3, sticky='e', padx=5, pady=5)
        Entry(self.frame_uno, textvariable=self.stock, width=25).grid(column=1, row=3, padx=5, pady=5)

        #Buttones de opciones
        Button(self.frame_uno, text='AGREGAR/ACTUALIZAR', font=('Arial', 10, 'bold'), command=self.agregar_actualizar,
               fg='black', bg='lime green', width=20, bd=3).grid(column=2, row=2, pady=5)
        
        Button(self.frame_uno, text='ELIMINAR', font=('Arial', 10, 'bold'), command=self.eliminar_datos,
               fg='black', bg='tomato', width=20, bd=3).grid(column=2, row=3, pady=5)

        Button(self.frame_uno, text='REFRESCAR', font=('Arial', 10, 'bold'), command=self.actualizar_tabla,
               fg='black', bg='deep sky blue', width=20, bd=3).grid(column=2, row=1, pady=5)
        
        Button(self.frame_uno, text='DESCARGAR EXCEL', font=('Arial', 10, 'bold'), command=self.descargar_excel,
               fg='black', bg='gold', width=20, bd=3).grid(column=2, row=4, pady=5)

        #Table
        self.tabla = ttk.Treeview(self.frame_dos, columns=('ID', 'Nombre', 'Descripción', 'Precio', 'Stock'), show='headings')
        self.tabla.grid(column=0, row=0, sticky='nsew')

        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150)

        #Scrollbar
        scroll = Scrollbar(self.frame_dos, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscroll=scroll.set)
        scroll.grid(column=1, row=0, sticky='ns')

        self.actualizar_tabla()

########################################

##Agregar


    def agregar_actualizar(self):
        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        precio = self.precio.get()
        stock = self.stock.get()

        if not nombre or not descripcion or not precio or not stock:
            messagebox.showwarning('Advertencia', 'Todos los campos son obligatorios')
            return

        self.base_datos.insterta_datos(nombre, descripcion, precio, stock)
        messagebox.showinfo('Información', 'Producto agregado/actualizado correctamente')
        self.actualizar_tabla()
        self.limpiar_campos()

################################

    ##Eliminar
    def eliminar_datos(self):
        seleccion = self.tabla.focus()

        if not seleccion:
            messagebox.showwarning('Advertencia', 'Debe seleccionar un producto para eliminar')
            return

        valores = self.tabla.item(seleccion, 'values') 
        id_producto = valores[0] 

        self.base_datos.elimina_datos(id_producto)
        messagebox.showinfo('Información', 'Producto eliminado correctamente')
        self.actualizar_tabla()

##############################

    ##Actualizar
    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        datos = self.base_datos.mostrar_datos()
        for fila in datos:
            self.tabla.insert('', 'end', values=fila)

    ##Descarga excell

    def descargar_excel(self):
        datos = self.base_datos.mostrar_datos()
        if not datos:
            messagebox.showwarning('Advertencia', 'No hay datos para exportar')
            return

        fecha = strftime('%d-%m-%y_%H-%M-%S')
        df = pd.DataFrame(datos, columns=['ID', 'Nombre', 'Descripción', 'Precio', 'Stock'])
        archivo = f'Datos_{fecha}.xlsx'
        df.to_excel(archivo, index=True)
        messagebox.showinfo('Información', f'Datos exportados a {archivo}')

    ##Limpia los campos
    def limpiar_campos(self):
        self.nombre.set('')
        self.descripcion.set('')
        self.precio.set('')
        self.stock.set('')

# Llamado al main
if __name__ == "__main__":
    ventana = Tk()
    ventana.title('Gestión de Productos')
    ventana.geometry('800x500')
    ventana.columnconfigure(0, weight=1)
    ventana.rowconfigure(0, weight=1)

    app = Ventana(ventana)
    app.grid(column=0, row=0, sticky="nsew") 

    ventana.mainloop()