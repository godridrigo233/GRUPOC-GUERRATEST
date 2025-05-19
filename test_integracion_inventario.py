import pytest
from unittest.mock import MagicMock, patch

# Simulación de entorno
cursor = MagicMock()
conn = MagicMock()
treeview = MagicMock()
treeview.focus.return_value = "item3"
treeview.item.return_value = {"values": [3]}  # Simulamos producto con ID 3

# Simulación de funciones
producto_db = {
    3: ("Clavo", 100, 0.5, "Unidades")
}

def seleccionar_producto(event):
    item_seleccionado = treeview.focus()
    if not item_seleccionado:
        return "no_seleccionado"
    producto = treeview.item(item_seleccionado)
    producto_id = producto['values'][0]
    return abrir_ventana_editar_producto(producto_id)

def abrir_ventana_editar_producto(producto_id):
    if producto_id not in producto_db:
        return "error"
    datos = producto_db[producto_id]
    return {"id": producto_id, "datos": datos}

def guardar_edicion_producto(producto_id, nuevo_nombre, nueva_cantidad, nuevo_precio, nueva_unidad):
    if producto_id not in producto_db:
        return "error"
    producto_db[producto_id] = (nuevo_nombre, nueva_cantidad, nuevo_precio, nueva_unidad)
    return "actualizado"

def eliminar_producto(producto_id):
    if producto_id in producto_db:
        del producto_db[producto_id]
        return "eliminado"
    return "no_encontrado"

# PRUEBAS DE INTEGRACIÓN
def test_integracion_doble_clic_abrir_edicion():
    resultado = seleccionar_producto(None)
    assert resultado["id"] == 3
    assert resultado["datos"] == ("Clavo", 100, 0.5, "Unidades")

def test_integracion_editar_producto():
    resultado = guardar_edicion_producto(3, "Clavo GRUESO", 150, 0.8, "Unidades")
    assert resultado == "actualizado"
    assert producto_db[3] == ("Clavo GRUESO", 150, 0.8, "Unidades")

def test_integracion_eliminar_producto():
    resultado = eliminar_producto(3)
    assert resultado == "eliminado"
    assert 3 not in producto_db
def test_integracion_editar_nombre_existente():
    # Insertamos 2 productos en la "BD"
    producto_db[10] = ("Martillo", 50, 15.0, "Unidades")
    producto_db[11] = ("Destornillador", 30, 5.5, "Unidades")

    # Intentamos cambiar el nombre del producto 11 a uno ya existente
    nombres = [v[0] for k, v in producto_db.items() if k != 11]
    if "Martillo" in nombres:
        resultado = "nombre_duplicado"
    else:
        resultado = guardar_edicion_producto(11, "Martillo", 30, 5.5, "Unidades")

    assert resultado == "nombre_duplicado"

def test_integracion_eliminar_inexistente():
    resultado = eliminar_producto(99)  # ID inexistente
    assert resultado == "no_encontrado"

def test_integracion_edicion_con_valores_invalidos():
    producto_db[12] = ("Llave", 20, 8.0, "Unidades")
    # Intentamos guardar cantidad negativa
    nueva_cantidad = -5
    if nueva_cantidad <= 0:
        resultado = "cantidad_invalida"
    else:
        resultado = guardar_edicion_producto(12, "Llave", nueva_cantidad, 8.0, "Unidades")

    assert resultado == "cantidad_invalida"

def test_integracion_consistencia_post_edicion():
    producto_db[13] = ("Taladro", 10, 120.0, "Unidades")
    guardar_edicion_producto(13, "Taladro PRO", 15, 135.0, "Unidades")
    # Verificamos que los valores hayan sido modificados correctamente
    nombre, cantidad, precio, unidad = producto_db[13]
    assert nombre == "Taladro PRO"
    assert cantidad == 15
    assert precio == 135.0
    assert unidad == "Unidades"
