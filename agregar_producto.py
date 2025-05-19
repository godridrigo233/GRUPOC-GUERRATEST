import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import mostrar_inventario  # Importamos para actualizar el inventario

# Obtener la ruta de la base de datos
ruta_directorio = os.path.dirname(os.path.abspath(__file__))
ruta_bd = os.path.join(ruta_directorio, 'ferreteria.db')

# Conexión a la base de datos
conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

# Crear la tabla de productos si no existe (sin el campo 'imagen')
cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    unidad TEXT)''')
conn.commit()

# Función para crear el frame de inventario
def crear_frame_inventario(root, frame_mostrar_inventario):
    frame_inventario = tk.Frame(root, bg="white")  # Fondo blanco para el frame principal
    frame_inventario.grid_columnconfigure(0, weight=1)  # Agregar espacio a la izquierda
    frame_inventario.grid_columnconfigure(3, weight=1)  # Agregar espacio a la derecha

    # Variables
    unidad_var = tk.StringVar(value="Selecciona tu unidad")
    opciones_unidad = ["Kilogramos", "Metros", "Unidades"]

    # Variable para el campo de nombre y función para transformar a mayúsculas
    nombre_var = tk.StringVar()
    
    def to_uppercase(*args):
        nombre_var.set(nombre_var.get().upper())

    nombre_var.trace_add("write", to_uppercase)

    # Cargar logo
    try:
        ruta_logo = os.path.join(ruta_directorio, 'logo.png')
        image = Image.open(ruta_logo)
        image = image.resize((200, 200), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(frame_inventario, image=logo, bg="white")
        logo_label.image = logo  # Mantener referencia
        logo_label.grid(row=0, column=1, columnspan=2, sticky="n", pady=(0, 20))
    except Exception as e:
        print(f"Error al cargar el logo: {e}")

    # Título del inventario
    titulo = tk.Label(frame_inventario, text="¡BIENVENIDO!\n AGREGA TU PRODUCTO", font=("Arial", 38, "bold"), pady=20, bg="white")
    titulo.grid(row=1, column=1, columnspan=2, sticky="nsew")

    # Campos de entrada en el orden deseado
    tk.Label(frame_inventario, text="NOMBRE", font=("Arial", 15, "bold"), bg="white").grid(row=2, column=1, sticky="e")
    entry_nombre = tk.Entry(frame_inventario, textvariable=nombre_var, width=30, font=("Arial", 16))
    entry_nombre.grid(row=2, column=2, padx=(10, 20), ipady=10)

    tk.Label(frame_inventario, text="CANTIDAD", font=("Arial", 15, "bold"), bg="white").grid(row=3, column=1, sticky="e")
    entry_cantidad = tk.Entry(frame_inventario, width=30, font=("Arial", 16))
    entry_cantidad.grid(row=3, column=2, padx=(10, 20), ipady=10)

    tk.Label(frame_inventario, text="UNIDAD", font=("Arial", 15, "bold"), bg="white").grid(row=4, column=1, sticky="e")
    menu_unidad = tk.OptionMenu(frame_inventario, unidad_var, *opciones_unidad)
    menu_unidad.config(width=20, font=("Arial", 16), bg="white")
    menu_unidad.grid(row=4, column=2, padx=(10, 20))

    # Ajustar tamaño de las opciones del menú desplegable
    menu_interno = frame_inventario.nametowidget(menu_unidad.menuname)
    menu_interno.config(font=("Arial", 16))  # Aplica el tamaño de fuente a las opciones

    tk.Label(frame_inventario, text="PRECIO", font=("Arial", 15, "bold"), bg="white").grid(row=5, column=1, sticky="e")
    entry_precio = tk.Entry(frame_inventario, width=30, font=("Arial", 16))
    entry_precio.grid(row=5, column=2, padx=(10, 20), ipady=10)
    productos_list = tk.Listbox(frame_inventario, width=80, height=10, bg="white")
    productos_list.grid(row=8, column=1, columnspan=2, pady=10)
    # Botón para agregar producto
    tk.Button(
        frame_inventario,
        text="Agregar producto",
        command=lambda: agregar_producto(entry_nombre, entry_cantidad, entry_precio, unidad_var, productos_list, frame_mostrar_inventario, mensaje_label),
        bg="orange",
        font=("Arial", 20, "bold")
    ).grid(row=6, column=1, columnspan=2, padx=(50, 5), pady=20, ipadx=30, ipady=10, sticky="ew")

    # Mensaje temporal en la parte inferior
    mensaje_label = tk.Label(frame_inventario, text="", font=("Arial", 12, "bold"), bg="white", fg="green")
    mensaje_label.grid(row=7, column=1, columnspan=2, pady=20)

    # Lista de productos (opcional)
    actualizar_lista_productos(productos_list)

    return frame_inventario
# Función para actualizar la lista de productos
def actualizar_lista_productos(productos_list):
    productos_list.delete(0, tk.END)
    cursor.execute('''SELECT nombre, cantidad, precio, unidad FROM productos''')
    for producto in cursor.fetchall():
        productos_list.insert(tk.END, f"{producto[0]} - Cantidad: {producto[1]} - Precio: {producto[2]:.2f} - Unidad: {producto[3]}")

def agregar_producto(entry_nombre, entry_cantidad, entry_precio, unidad_var, productos_list, frame_mostrar_inventario, mensaje_label):
    nombre = entry_nombre.get().strip()
    cantidad = entry_cantidad.get().strip()
    precio = entry_precio.get().strip()
    unidad = unidad_var.get().strip()

    # Verificar que todos los campos están llenos
    if not nombre or not cantidad or not precio:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    # Validación nueva: nombre no debe exceder los 31 caracteres
    if len(nombre) > 31:
        messagebox.showerror("Error", "El nombre no debe exceder los 31 caracteres.")
        return

    # Verificar si se ha seleccionado una unidad válida
    if unidad == "Selecciona tu unidad":
        messagebox.showerror("Error", "Debes elegir una unidad.")
        return

    try:
        # Validar que la cantidad sea un número
        try:
            cantidad_valor = float(cantidad)
        except ValueError:
            messagebox.showerror("Error", "La cantidad ingresada no es un número válido.")
            return

        # Validar que el precio sea un número
        try:
            precio_valor = float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio ingresado no es un número válido.")
            return
        
        
        # Convertir cantidad y precio a valores numéricos
        if unidad == "Metros":
            cantidad = float(cantidad)
        else:
            cantidad = float(cantidad)

        precio = round(float(precio), 2)


        # Verificar que cantidad y precio sean positivos
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un monto positivo.")
            return

        if precio <= 0:
            messagebox.showerror("Error", "El precio debe ser un monto positivo.")
            return

        # Nueva validación: cantidad no debe ser mayor a 1000
        if cantidad > 1000:
            messagebox.showerror("Error", "La cantidad no puede ser mayor a 1000.")
            return

        # Nueva validación: precio no debe ser mayor a 1000
        if precio > 1000:
            messagebox.showerror("Error", "El precio no puede ser mayor a 1000.")
            return

        # Validar decimales para unidades
        if cantidad % 1 != 0 and unidad == "Unidades":
            messagebox.showerror("Error", "No se admiten valores decimales para unidad de medida: Unidades.")
            return

        # Verificar si el producto ya existe en la base de datos
        cursor.execute('''SELECT COUNT(*) FROM productos WHERE nombre = ?''', (nombre,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "Ya existe un producto con este nombre.")
            return

        # Insertar el producto en la base de datos
        cursor.execute('''INSERT INTO productos (nombre, cantidad, precio, unidad) 
                          VALUES (?, ?, ?, ?)''', (nombre, cantidad, precio, unidad))
        conn.commit()

        # Actualizar la lista de productos en la interfaz
        actualizar_lista_productos(productos_list)

        # Mostrar mensaje temporal de éxito
        mensaje_label.config(text="¡Producto agregado!", bg="green", fg="white", font=("Arial", 35, "bold"))
        mensaje_label.after(3200, lambda: mensaje_label.config(text="", bg="white"))
        # Limpiar los campos después de agregar el producto
        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        unidad_var.set("Selecciona tu unidad")
    
    except Exception as e:
        messagebox.showerror("Error inesperado", f"Ocurrió un error: {str(e)}")


# Función para configurar el botón "Volver"
def configurar_boton_volver(frame_inventario, comando_volver):
    btn_volver = tk.Button(frame_inventario, text="Volver al menú principal", command=comando_volver, width=25, height=3, font=("Arial", 12), bg="red", fg="white")
    btn_volver.grid(row=9, column=1, pady=15)
