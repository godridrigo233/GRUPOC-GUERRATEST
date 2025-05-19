import pytest
from unittest.mock import MagicMock

# Simulaciones necesarias
treeview = MagicMock()
treeview.get_children.return_value = ['item1', 'item2']
treeview.delete = MagicMock()
treeview.insert = MagicMock()
treeview.tag_configure = MagicMock()

cursor = MagicMock()
entry = MagicMock()

# Función simulada de búsqueda de productos
def buscar_producto(entry_busqueda, treeview):
    termino = entry_busqueda.get().strip()
    if not termino:
        return "actualizar"

    cursor.execute("SELECT id, nombre, cantidad, unidad, precio FROM productos WHERE nombre LIKE ? ORDER BY nombre", (f"%{termino}%",))
    productos = cursor.fetchall()

    for item in treeview.get_children():
        treeview.delete(item)

    if not productos:
        return "vacio"

    for index, producto in enumerate(productos):
        tags = 'evenrow' if index % 2 == 0 else 'oddrow'
        treeview.insert("", "end", values=(producto[0], producto[1], producto[2], producto[3], f"{producto[4]:.2f}"), tags=(tags,))
    return "ok"

# ---------- PRUEBAS ----------

def test_busqueda_vacia():
    entry.get.return_value = ""
    assert buscar_producto(entry, treeview) == "actualizar"

def test_busqueda_sin_resultados():
    entry.get.return_value = "inexistente"
    cursor.fetchall.return_value = []
    assert buscar_producto(entry, treeview) == "vacio"

def test_busqueda_exitosa():
    entry.get.return_value = "Martillo"
    cursor.fetchall.return_value = [(1, "Martillo", 5, "Unidades", 12.5)]
    assert buscar_producto(entry, treeview) == "ok"

def test_busqueda_con_espacios():
    entry.get.return_value = "  tornillo   "
    cursor.fetchall.return_value = [(2, "Tornillo", 20, "Unidades", 1.2)]
    assert buscar_producto(entry, treeview) == "ok"

def test_busqueda_mayus_minus():
    entry.get.return_value = "clavo"
    cursor.fetchall.return_value = [(3, "Clavo", 100, "Unidades", 0.5)]
    assert buscar_producto(entry, treeview) == "ok"

def test_busqueda_caracteres_especiales():
    entry.get.return_value = "@@@"
    cursor.fetchall.return_value = []
    assert buscar_producto(entry, treeview) == "vacio"

def test_borra_contenido_treeview():
    treeview.delete.reset_mock() 
    entry.get.return_value = "alicate"
    cursor.fetchall.return_value = [(4, "Alicate", 8, "Unidades", 9.99)]
    buscar_producto(entry, treeview)
    assert treeview.delete.call_count == len(treeview.get_children())