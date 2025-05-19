import pytest
from tkinter import messagebox
from unittest.mock import MagicMock, patch

# Simulamos funciones externas
def actualizar_frame_inventario():
    pass

def cerrar_ventana_editar():
    pass

# Base de datos simulada
class MockCursor:
    def __init__(self):
        self.existing_names = {}

    def execute(self, query, params):
        if "SELECT id FROM productos" in query:
            nombre, producto_id = params
            if nombre in self.existing_names and self.existing_names[nombre] != producto_id:
                self.result = [(1,)]
            else:
                self.result = []
        elif "UPDATE productos" in query:
            self.updated = True

    def fetchone(self):
        return self.result[0] if self.result else None

cursor = MockCursor()
conn = MagicMock()
producto_id = 1
entry_nombre = MagicMock()
entry_cantidad = MagicMock()
entry_precio = MagicMock()
unidad_var = MagicMock()
ventana_editar = MagicMock()

def guardar_cambios():
    nuevo_nombre = entry_nombre.get().strip()
    nueva_cantidad = entry_cantidad.get().strip()
    nueva_unidad = unidad_var.get()
    nuevo_precio = entry_precio.get().strip()

    cursor.execute("SELECT id FROM productos WHERE nombre = ? AND id != ?", (nuevo_nombre, producto_id))
    if cursor.fetchone() is not None:
        messagebox.showerror("Error", "Ya existe otro producto con ese nombre.")
        ventana_editar.lift()
        return

    if not nuevo_nombre or not nueva_cantidad or not nuevo_precio:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        ventana_editar.lift()
        return

    if len(nuevo_nombre) > 31:
        messagebox.showerror("Error", "El nombre no debe exceder los 31 caracteres.")
        ventana_editar.lift()
        return

    try:
        nueva_cantidad = float(nueva_cantidad)
    except ValueError:
        messagebox.showerror("Error", "La cantidad debe ser un número válido. Ej: 5 o 2.5")
        ventana_editar.lift()
        return

    try:
        nuevo_precio = round(float(nuevo_precio), 2)
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número válido. Ej: 10.99")
        ventana_editar.lift()
        return

    if nueva_unidad == "Unidades" and not nueva_cantidad.is_integer():
        messagebox.showerror("Error", "La cantidad debe ser un número entero cuando la unidad es 'Unidades'.")
        ventana_editar.lift()
        return

    if nueva_cantidad <= 0:
        messagebox.showerror("Error", "La cantidad debe ser mayor a cero.")
        ventana_editar.lift()
        return

    if nueva_cantidad > 1000:
        messagebox.showerror("Error", "La cantidad no puede ser mayor a 1000.")
        ventana_editar.lift()
        return

    if nuevo_precio <= 0:
        messagebox.showerror("Error", "El precio debe ser mayor a cero.")
        ventana_editar.lift()
        return

    if nuevo_precio > 1000:
        messagebox.showerror("Error", "El precio no puede ser mayor a 1000.")
        ventana_editar.lift()
        return

    cursor.execute("SELECT id FROM productos WHERE nombre = ? AND id != ?", (nuevo_nombre, producto_id))
    if cursor.fetchone():
        messagebox.showerror("Error", f"Ya existe otro producto con el nombre '{nuevo_nombre}'.")
        ventana_editar.lift()
        return

    cursor.execute(
        "UPDATE productos SET nombre=?, cantidad=?, precio=?, unidad=? WHERE id=?",
        (nuevo_nombre, nueva_cantidad, nuevo_precio, nueva_unidad, producto_id)
    )
    conn.commit()

    cerrar_ventana_editar()
    messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
    actualizar_frame_inventario()

# PRUEBAS
@patch('tkinter.messagebox.showerror')
def test_campo_vacio(mock_error):
    entry_nombre.get.return_value = ""
    entry_cantidad.get.return_value = "5"
    entry_precio.get.return_value = "10"
    unidad_var.get.return_value = "Unidades"
    guardar_cambios()
    mock_error.assert_called_with("Error", "Todos los campos son obligatorios.")

@patch('tkinter.messagebox.showerror')
def test_nombre_largo(mock_error):
    entry_nombre.get.return_value = "X" * 32
    entry_cantidad.get.return_value = "5"
    entry_precio.get.return_value = "10"
    unidad_var.get.return_value = "Unidades"
    guardar_cambios()
    mock_error.assert_called_with("Error", "El nombre no debe exceder los 31 caracteres.")

@patch('tkinter.messagebox.showerror')
def test_precio_invalido(mock_error):
    entry_nombre.get.return_value = "Producto"
    entry_cantidad.get.return_value = "5"
    entry_precio.get.return_value = "abc"
    unidad_var.get.return_value = "Unidades"
    guardar_cambios()
    mock_error.assert_called_with("Error", "El precio debe ser un número válido. Ej: 10.99")

@patch('tkinter.messagebox.showerror')
def test_cantidad_negativa(mock_error):
    entry_nombre.get.return_value = "Producto válido"
    entry_cantidad.get.return_value = "-5"
    entry_precio.get.return_value = "10"
    unidad_var.get.return_value = "Kilogramos"
    guardar_cambios()
    mock_error.assert_called_with("Error", "La cantidad debe ser mayor a cero.")

@patch('tkinter.messagebox.showerror')
def test_decimal_con_unidades(mock_error):
    entry_nombre.get.return_value = "Producto válido"
    entry_cantidad.get.return_value = "3.5"
    entry_precio.get.return_value = "10"
    unidad_var.get.return_value = "Unidades"
    guardar_cambios()
    mock_error.assert_called_with("Error", "La cantidad debe ser un número entero cuando la unidad es 'Unidades'.")

@patch('tkinter.messagebox.showerror')
def test_nombre_duplicado(mock_error):
    cursor.existing_names = {"Producto duplicado": 99}  # Simula existencia con distinto ID
    entry_nombre.get.return_value = "Producto duplicado"
    entry_cantidad.get.return_value = "10"
    entry_precio.get.return_value = "15"
    unidad_var.get.return_value = "Metros"
    guardar_cambios()
    mock_error.assert_called_with("Error", "Ya existe otro producto con ese nombre.")
    cursor.existing_names = {}  # Limpiar para otros tests

@patch('tkinter.messagebox.showinfo')
def test_ingreso_correcto(mock_info):
    entry_nombre.get.return_value = "Nuevo Producto"
    entry_cantidad.get.return_value = "20"
    entry_precio.get.return_value = "9.99"
    unidad_var.get.return_value = "Kilogramos"
    guardar_cambios()
    mock_info.assert_called_with("Éxito", "Producto actualizado correctamente.")
