
import pytest

inventario = []

def agregar_producto(nombre, cantidad, unidad, precio):
    if not nombre or not cantidad or not unidad or not precio:
        return "campos_vacios"
    if any(p['nombre'].strip().lower() == nombre.strip().lower() for p in inventario):
        return "duplicado"
    try:
        cantidad = float(cantidad)
        precio = float(precio)
    except ValueError:
        return "no_numerico"
    inventario.append({
        "nombre": nombre,
        "cantidad": cantidad,
        "unidad": unidad,
        "precio": round(precio, 2)
    })
    return "agregado"

# Nuevas pruebas para encontrar fallos adicionales
def test_duplicado_case_insensitive():
    inventario.clear()
    agregar_producto("Martillo", "5", "Unidades", "20")
    resultado = agregar_producto("MARTILLO", "2", "Unidades", "25")
    assert resultado == "duplicado"

def test_nombre_con_caracteres_invalidos():
    inventario.clear()
    resultado = agregar_producto("Taladro@123", "1", "Unidades", "10")
    assert resultado != "agregado"

def test_precio_con_espacios():
    inventario.clear()
    resultado = agregar_producto("Sierra", "3", "Unidades", " 25 ")
    assert resultado == "agregado"

def test_agregar_producto_sin_redondeo_precio():
    inventario.clear()
    agregar_producto("Clavo", "2", "Unidades", "5.6789")
    assert inventario[0]["precio"] == 5.68

def test_cantidad_con_formato_invalido():
    inventario.clear()
    resultado = agregar_producto("Tuerca", "5kg", "Unidades", "1.5")
    assert resultado != "agregado"
