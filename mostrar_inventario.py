import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, PhotoImage
from PIL import Image, ImageTk  # Importamos Image y ImageTk de Pillow
import sqlite3
import os

# Conexión a la base de datos
ruta_directorio = os.path.dirname(os.path.abspath(__file__))
ruta_bd = os.path.join(ruta_directorio, 'ferreteria.db')
conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

def crear_frame_mostrar_inventario(root):
    frame_mostrar_inventario = tk.Frame(root, bg="white")

    # Título en la parte superior
    titulo = tk.Label(frame_mostrar_inventario, text="INVENTARIO - FERRETERÍA RUPHA", font=("Arial", 35, "bold"), bg="white", fg="black")
    titulo.pack(pady=20)

    # Cargar y colocar el logo en la esquina superior derecha
    ruta_logo = os.path.join(ruta_directorio, 'logo.png')

    if os.path.exists(ruta_logo):
        try:
            # Cargar la imagen y redimensionarla si es necesario
            logo_image = Image.open(ruta_logo)
            logo_image = logo_image.resize((95, 95), Image.LANCZOS)  # Cambia el tamaño según sea necesario
            logo_photo = ImageTk.PhotoImage(logo_image)

            # Colocar el logo en la esquina superior derecha
            logo_label = tk.Label(frame_mostrar_inventario, image=logo_photo, bg="white")
            logo_label.image = logo_photo  # Mantener referencia
            logo_label.place(relx=1.0, y=14, anchor="ne", x=-20)  # Ajusta 'y' para desplazar hacia abajo

        except Exception as e:
            print(f"Error al cargar el logo: {e}")
    else:
        print("El archivo 'logo.png' no se encontró en la ruta especificada.")

    # Barra de búsqueda debajo del título
    busqueda_frame = tk.Frame(frame_mostrar_inventario, bg="white")
    busqueda_frame.pack(fill="x", padx=20)

    # Entrada de búsqueda
    entry_busqueda = tk.Entry(busqueda_frame, width=30, font=("Arial", 16))
    entry_busqueda.pack(side="left", padx=10, pady=10)

    # Vincular el evento de búsqueda en tiempo real
    entry_busqueda.bind("<KeyRelease>", lambda event: buscar_producto(entry_busqueda, treeview))

    # Botón de búsqueda con ícono de lupa
    ruta_lupa = os.path.join(ruta_directorio, 'lupa.png')  # Ruta del icono de lupa
    if os.path.exists(ruta_lupa):
        lupa_image = Image.open(ruta_lupa)
        lupa_image = lupa_image.resize((30, 30), Image.LANCZOS)
        lupa_photo = ImageTk.PhotoImage(lupa_image)

        boton_buscar = tk.Button(
            busqueda_frame,
            image=lupa_photo,
            bg="white",
            command=lambda: buscar_producto(entry_busqueda, treeview),
            borderwidth=0
        )
        boton_buscar.image = lupa_photo
        boton_buscar.pack(side="left", padx=10)

    # Estilo personalizado para Treeview
    estilo = ttk.Style()
    estilo.configure("Treeview", font=("Arial", 14), rowheight=30)
    estilo.configure("Treeview.Heading", font=("Arial", 16, "bold"))

    # Crear Treeview para mostrar el inventario
    tree_frame = tk.Frame(frame_mostrar_inventario)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Definir el Treeview con columnas
    global treeview  # Declaración global para que la función de actualización pueda acceder
    columns = ("ID", "Nombre", "Cantidad", "Unidad", "Precio")
    treeview = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
    treeview.pack(side="left", fill="both", expand=True)

    # Configurar encabezados de las columnas
    treeview.heading("ID", text="ID")
    treeview.heading("Nombre", text="Nombre")
    treeview.heading("Cantidad", text="Cantidad")
    treeview.heading("Unidad", text="Unidad")
    treeview.heading("Precio", text="Precio")

    # Configurar ancho y alineación de las columnas
    treeview.column("ID", width=10, anchor="center")
    treeview.column("Nombre", width=200, anchor="center")
    treeview.column("Cantidad", width=100, anchor="center")
    treeview.column("Unidad", width=100, anchor="center")
    treeview.column("Precio", width=60, anchor="center")

    # Scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=treeview.yview)
    scrollbar.pack(side="right", fill="y")
    treeview.config(yscrollcommand=scrollbar.set)

    # Configurar el evento de clic en el Treeview
    treeview.bind("<Double-1>", seleccionar_producto)

    return frame_mostrar_inventario

# Función para buscar productos en tiempo real
def buscar_producto(entry_busqueda, treeview):
    termino = entry_busqueda.get().strip()
    if not termino:
        actualizar_frame_inventario()
        return

    # Realizar consulta para buscar coincidencias
    cursor.execute('''SELECT id, nombre, cantidad, unidad, precio 
                       FROM productos WHERE nombre LIKE ? ORDER BY nombre''', (f"%{termino}%",))
    productos = cursor.fetchall()

    # Limpiar el Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Mostrar resultados en el Treeview
    if productos:
        for index, producto in enumerate(productos):
            tags = 'evenrow' if index % 2 == 0 else 'oddrow'
            treeview.insert("", "end", values=(producto[0], producto[1], producto[2], producto[3], f"{producto[4]:.2f}"), tags=(tags,))
        treeview.tag_configure('evenrow', background='white')
        treeview.tag_configure('oddrow', background='#E8E8E8')
    # SI NO HAY RESULTADO NO SE MUESTRA NADA

        
# Función para obtener los productos de la base de datos
def obtener_productos():
    cursor.execute('SELECT id, nombre, cantidad, unidad, precio FROM productos')
    return cursor.fetchall()

# Función para actualizar el Treeview con el inventario
def actualizar_frame_inventario():
    # Limpiar el contenido actual del Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Obtener y mostrar los productos actualizados desde la base de datos
    cursor.execute('SELECT id, nombre, cantidad, unidad, precio FROM productos')
    productos = cursor.fetchall()

    # Si no hay productos, mostrar un mensaje de inventario vacío
    if not productos:
        messagebox.showinfo("Inventario vacío", "No hay productos en el inventario.")
        return

    # Alternar el color de las filas y añadir los datos al Treeview
    for index, producto in enumerate(productos):
        tags = 'evenrow' if index % 2 == 0 else 'oddrow'
        treeview.insert("", "end", values=(producto[0], producto[1], producto[2], producto[3], f"{producto[4]:.2f}"), tags=(tags,))

    # Configurar los colores para las filas
    treeview.tag_configure('evenrow', background='white')    # Blanco o color claro
    treeview.tag_configure('oddrow', background='#E8E8E8')   # Gris o color oscuro

# Variable global para la ventana de edición
ventana_editar = None

# Función para abrir la ventana de edición de un producto
def abrir_ventana_editar_producto(producto_id):
    global ventana_editar

    # Verificar si la ventana ya está abierta
    if ventana_editar is not None and ventana_editar.winfo_exists():
        ventana_editar.lift()  # Llevar la ventana al frente si ya está abierta
        return

    # Obtener los datos actuales del producto seleccionado
    cursor.execute("SELECT nombre, cantidad, precio, unidad FROM productos WHERE id=?", (producto_id,))
    producto = cursor.fetchone()
    if not producto:
        messagebox.showerror("Error", "No se pudo encontrar el producto.")
        return

    nombre_actual, cantidad_actual, precio_actual, unidad_actual = producto

    # Crear la ventana de edición
    ventana_editar = Toplevel()
    ventana_editar.title("EDITAR PRODUCTO")
    ventana_editar.configure(bg="white")

    # Centrando la ventana en la pantalla
    window_width = 540
    window_height = 450
    screen_width = ventana_editar.winfo_screenwidth()
    screen_height = ventana_editar.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    ventana_editar.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    # Variables
    nombre_var = tk.StringVar(value=nombre_actual)

    # Función para convertir el texto a mayúsculas en tiempo real
    def to_uppercase(*args):
        nombre_var.set(nombre_var.get().upper())

    # Añadir el trace para el cambio en tiempo real
    nombre_var.trace_add("write", to_uppercase)

    # Título
    titulo = tk.Label(ventana_editar, text="EDITA TU PRODUCTO", font=("Arial", 20, "bold"), pady=10, bg="white")
    titulo.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Campos de edición organizados con `grid`
    tk.Label(ventana_editar, text="NOMBRE", font=("Arial", 15, "bold"), bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_nombre = tk.Entry(ventana_editar, textvariable=nombre_var, width=30, font=("Arial", 16))
    entry_nombre.grid(row=1, column=1, padx=(10, 20), pady=5, sticky="w")

    tk.Label(ventana_editar, text="CANTIDAD", font=("Arial", 15, "bold"), bg="white").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_cantidad = tk.Entry(ventana_editar, width=30, font=("Arial", 16))
    entry_cantidad.insert(0, cantidad_actual)
    entry_cantidad.grid(row=2, column=1, padx=(10, 20), pady=5, sticky="w")

    tk.Label(ventana_editar, text="UNIDAD", font=("Arial", 15, "bold"), bg="white").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    unidad_var = tk.StringVar(value=unidad_actual)
    opciones_unidad = ["Kilogramos", "Gramos", "Unidades"]

    # Evitar duplicados en las opciones del menú desplegable
    if unidad_actual not in opciones_unidad:
        opciones_unidad.insert(0, unidad_actual)

    menu_unidad = tk.OptionMenu(ventana_editar, unidad_var, *opciones_unidad)
    menu_unidad.config(width=20, font=("Arial", 16), bg="white")
    menu_unidad.grid(row=3, column=1, padx=(10, 20), pady=5, sticky="w")

    # Ajustar tamaño de las opciones del menú desplegable
    menu_interno = ventana_editar.nametowidget(menu_unidad.menuname)
    menu_interno.config(font=("Arial", 12))

    tk.Label(ventana_editar, text="PRECIO", font=("Arial", 15, "bold"), bg="white").grid(row=4, column=0, sticky="e", padx=10, pady=5)
    entry_precio = tk.Entry(ventana_editar, width=30, font=("Arial", 16))
    entry_precio.insert(0, "{:.2f}".format(precio_actual))  # Formato de dos decimales
    entry_precio.grid(row=4, column=1, padx=(10, 20), pady=5, sticky="w")

    # Función para guardar los cambios
    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nueva_cantidad = entry_cantidad.get()
        nueva_unidad = unidad_var.get()
        nuevo_precio = entry_precio.get()

        if not nuevo_nombre or not nueva_cantidad or not nuevo_precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            # Traer la ventana de edición al frente
            ventana_editar.lift()
            return

        try:
            nueva_cantidad = float(nueva_cantidad)
            nuevo_precio = float(nuevo_precio)

            # Actualizar el producto en la base de datos
            cursor.execute('''UPDATE productos SET nombre=?, cantidad=?, precio=?, unidad=? WHERE id=?''',
                        (nuevo_nombre, nueva_cantidad, nuevo_precio, nueva_unidad, producto_id))
            conn.commit()

            # Cerrar la ventana de edición y mostrar mensaje solo si no hay errores
            cerrar_ventana_editar()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            actualizar_frame_inventario()  # Actualizar el inventario

        except ValueError:
            # Mostrar mensaje de error, mantener la ventana abierta y traerla al frente
            messagebox.showerror("Error", "Cantidad y precio deben ser números.")
            ventana_editar.lift()  # Traer la ventana al frente

    # Al abrir la ventana de edición, asegúrate de traerla al frente
    ventana_editar.lift()

    # Botón para guardar los cambios
    btn_guardar = tk.Button(
        ventana_editar, 
        text="Guardar cambios", 
        command=guardar_cambios, 
        bg="#4CAF50",  # Fondo verde
        fg="white",    # Texto blanco
        font=("Arial", 14, "bold")
    )
    btn_guardar.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    # Espaciador para bajar el botón de eliminar
    espaciador = tk.Label(ventana_editar, text="", bg="white")
    espaciador.grid(row=6, column=0, columnspan=2, pady=(10, 30))

    # Función para eliminar el producto
    def eliminar_producto():
        respuesta = messagebox.askyesno("Eliminar Producto", "¿Estás seguro de que deseas eliminar este producto?")
        if respuesta:
            cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
            conn.commit()
            cerrar_ventana_editar()
            messagebox.showinfo("PRODUCTO ELIMINADO", "El producto ha sido eliminado correctamente.")
            actualizar_frame_inventario()  # Actualizar el inventario

    # Botón para eliminar el producto
    btn_eliminar = tk.Button(
        ventana_editar, 
        text="Eliminar producto", 
        command=eliminar_producto, 
        bg="#FF5733",  # Fondo rojo
        fg="white",    # Texto blanco
        font=("Arial", 14, "bold")
    )
    btn_eliminar.grid(row=7, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")

    # Configurar el cierre de la ventana
    ventana_editar.protocol("WM_DELETE_WINDOW", cerrar_ventana_editar)

# Función para cerrar la ventana de edición
def cerrar_ventana_editar():
    global ventana_editar
    if ventana_editar is not None:
        ventana_editar.destroy()
        ventana_editar = None

# Función para seleccionar el producto y abrir la ventana de edición
def seleccionar_producto(event):
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)
        producto_id = item['values'][0]  # El ID está en la primera columna
        abrir_ventana_editar_producto(producto_id)
