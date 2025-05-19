
import pytest

inventario = []

def agregar_producto(nombre, cantidad, unidad, precio):
    # Función simulada con errores posibles
    if not nombre or not cantidad or not unidad or not precio:
        return "campos_vacios"
    if any(p['nombre'] == nombre for p in inventario):
        return "duplicado"
    try:
        cantidad = float(cantidad)
        precio = float(precio)
    except ValueError:
        return "no_numerico"
    # Error posible: no se valida si son negativos o cero
    inventario.append({
        "nombre": nombre,
        "cantidad": cantidad,
        "unidad": unidad,
        "precio": round(precio, 2)
    })
    return "agregado"

def buscar_producto(nombre):
    return [p for p in inventario if nombre.lower() in p['nombre'].lower()]

# TESTS PARA ENCONTRAR ERRORES

def test_no_valida_negativo_en_cantidad():
    inventario.clear()
    resultado = agregar_producto("Clavo", "-5", "Unidades", "10")
    assert resultado != "agregado"  # Debería rechazar, pero no lo hace

def test_no_valida_precio_cero():
    inventario.clear()
    resultado = agregar_producto("Tornillo", "10", "Unidades", "0")
    assert resultado != "agregado"

def test_acepta_nombre_con_espacios_solo():
    inventario.clear()
    resultado = agregar_producto("   ", "10", "Unidades", "10")
    assert resultado != "agregado"

def test_nombre_muy_largo_no_restringido():
    inventario.clear()
    nombre_largo = "A" * 100
    resultado = agregar_producto(nombre_largo, "5", "Unidades", "12")
    assert resultado != "agregado"

def test_acepta_precio_no_redondeado():
    inventario.clear()
    agregar_producto("Taladro", "2", "Unidades", "19.9999")
    assert any(p["precio"] == 20.0 for p in inventario)  # Redondeo mal hecho

def test_busqueda_case_sensitive():
    inventario.clear()
    agregar_producto("Destornillador", "1", "Unidades", "5")
    resultados = buscar_producto("destornillador")
    assert len(resultados) == 1  # Si no encuentra, es un bug de sensibilidad

def test_permite_producto_sin_unidad():
    inventario.clear()
    resultado = agregar_producto("Alicate", "2", "", "15")
    assert resultado != "agregado"

def test_no_rechaza_precio_con_letras():
    inventario.clear()
    resultado = agregar_producto("Martillo", "1", "Unidades", "15usd")
    assert resultado != "agregado"

def test_no_detecta_duplicado_si_cambia_cantidad():
    inventario.clear()
    agregar_producto("Clavo", "5", "Unidades", "2")
    resultado = agregar_producto("Clavo", "10", "Unidades", "2")
    assert resultado == "duplicado"  # Debería rechazar aunque cambie cantidad

def test_no_valida_unidad_fuera_de_opciones():
    inventario.clear()
    resultado = agregar_producto("Llave", "1", "Docenas", "3")
    assert resultado != "agregado"
