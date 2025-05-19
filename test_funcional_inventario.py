import pytest
from unittest.mock import MagicMock

# Simulamos base de datos de productos
inventario = []

def agregar_producto(nombre, cantidad, unidad, precio):
    if not nombre or not cantidad or not unidad or not precio:
        return "campos_vacios"
    if any(p['nombre'] == nombre for p in inventario):
        return "duplicado"
    try:
        cantidad = float(cantidad)
        precio = float(precio)
    except ValueError:
        return "no_numerico"
    if cantidad <= 0 or precio <= 0:
        return "valores_invalidos"
    inventario.append({
        "nombre": nombre,
        "cantidad": cantidad,
        "unidad": unidad,
        "precio": round(precio, 2)
    })
    return "agregado"

def buscar_producto(nombre):
    return [p for p in inventario if nombre.lower() in p['nombre'].lower()]

def descargar_reporte():
    return "reporte_generado" if inventario else "sin_datos"

# -------- PRUEBAS FUNCIONALES --------
def test_funcional_agregar_correcto():
    inventario.clear()
    resultado = agregar_producto("Taladro", "5", "Unidades", "150.50")
    assert resultado == "agregado"
    assert inventario[0]['nombre'] == "Taladro"

def test_funcional_agregar_duplicado():
    inventario.clear()
    agregar_producto("Martillo", "3", "Unidades", "25")
    resultado = agregar_producto("Martillo", "5", "Unidades", "30")
    assert resultado == "duplicado"

def test_funcional_buscar_existente():
    inventario.clear()
    agregar_producto("Destornillador", "7", "Unidades", "15")
    resultados = buscar_producto("dest")
    assert len(resultados) == 1
    assert resultados[0]['nombre'] == "Destornillador"

def test_funcional_descargar_reporte_con_datos():
    inventario.clear()
    agregar_producto("Llave", "10", "Unidades", "40")
    resultado = descargar_reporte()
    assert resultado == "reporte_generado"

def test_funcional_descargar_reporte_vacio():
    inventario.clear()
    resultado = descargar_reporte()
    assert resultado == "sin_datos"
def test_funcional_agregar_valores_invalidos():
    inventario.clear()
    resultado = agregar_producto("Cinta", "-3", "Metros", "5")
    assert resultado == "valores_invalidos"

def test_funcional_agregar_con_campos_vacios():
    inventario.clear()
    resultado = agregar_producto("", "2", "Unidades", "10")
    assert resultado == "campos_vacios"

def test_funcional_agregar_precio_no_numerico():
    inventario.clear()
    resultado = agregar_producto("Pegamento", "3", "Unidades", "abc")
    assert resultado == "no_numerico"

def test_funcional_buscar_inexistente():
    inventario.clear()
    agregar_producto("Sierra", "1", "Unidades", "70")
    resultados = buscar_producto("alicate")
    assert len(resultados) == 0
