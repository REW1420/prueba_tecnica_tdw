

movimientos = [
    {"producto": "A", "tipo": "entrada", "cantidad": 20},
    {"producto": "A", "tipo": "salida", "cantidad": 3},
    {"producto": "B", "tipo": "entrada", "cantidad": 5},
    {"producto": "A", "tipo": "entrada", "cantidad": 2},
    {"producto": "B", "tipo": "salida", "cantidad": -5},
    {"producto": "B", "tipo": "entrada", "cantidad": 10},
    {"producto": "A", "tipo": " salida ", "cantidad": 9},
    {"producto": "B", "tipo": "salida", "cantidad": -5},
]

estados = [
    {"producto": "A", "estado": "disponible "},
    {"producto": "B", " estado ": "disponible"},
    {"producto": "C", " estado ": "descontinuado"},
]


def normalizar_registro(registro):
    """Quita espacios de los nombres de campos y de los valores de texto."""
    return {
        str(clave).strip(): valor.strip() if isinstance(valor, str) else valor
        for clave, valor in registro.items()
    }


estados_por_producto = {}
for estado in estados:
    estado = normalizar_registro(estado)
    producto = str(estado.get("producto", "")).strip()
    if producto:
        estados_por_producto[producto] = str(estado.get("estado", "")).strip().casefold()

productos_descontinuados = {
    producto
    for producto, estado in estados_por_producto.items()
    if estado == "descontinuado"
}

# Inicializar los productos conocidos no descontinuados para incluir también aquellos cuyo inventario final sea cero
inventario = {
    producto: 0
    for producto in estados_por_producto
    if producto not in productos_descontinuados
}
movimientos_invalidos = []

for numero, movimiento in enumerate(movimientos, start=1):
    movimiento = normalizar_registro(movimiento)
    producto = str(movimiento.get("producto", "")).strip()

    # ignorar por completo los movimientos de productos descontinuados.
    if producto in productos_descontinuados:
        continue

    tipo = str(movimiento.get("tipo", "")).strip().casefold()
    cantidad_original = movimiento.get("cantidad")

    try:
        cantidad = float(cantidad_original)
    except (TypeError, ValueError):
        movimientos_invalidos.append((numero, movimiento, "cantidad no numérica"))
        continue

    if not producto:
        movimientos_invalidos.append((numero, movimiento, "falta el producto"))
        continue
    if tipo not in ("entrada", "salida"):
        movimientos_invalidos.append((numero, movimiento, "tipo debe ser 'entrada' o 'salida'"))
        continue
    if cantidad < 0:
        movimientos_invalidos.append((numero, movimiento, "la cantidad no puede ser negativa"))
        continue

    inventario.setdefault(producto, 0)

    if tipo == "entrada":
        inventario[producto] += cantidad
    elif cantidad > inventario[producto]:
        movimientos_invalidos.append((numero, movimiento, "la salida dejaría el inventario negativo"))
    else:
        inventario[producto] -= cantidad


print("Inventario final (de mayor a menor):")
for producto, cantidad in sorted(inventario.items(), key=lambda item: (-item[1], item[0].casefold())):
    print(f"{producto}: {cantidad:g}")

print("\nMovimientos inválidos:")
if movimientos_invalidos:
    for numero, movimiento, motivo in movimientos_invalidos:
        print(f"Movimiento {numero}: {movimiento} — {motivo}")
else:
    print("Ninguno")

#	¿Qué mejorarías si este código fuera a producción?
# me gustaria delegar mas sub funciones, y añadir un poco de mas validaciones extras, al codigo le falta un poco mas de robustes posiblemente llegara a fallar a grandes listas
# me gustaria tambien mejorar el tipo de objeto que se recibe evitando numeros negativos y solo definiendo el tipo de movimiento asi no se llegan a generar errores de comprension

#	¿Qué complejidad tiene tu solución?

# no considero que la colucion tenga alta complejidad pero a largo podria generar problemas de entendimiento, aun asi diria que tiene complejidad constante 0(1)

#	¿Cómo probarías tu implementación?
# me gustaria probarlo con inventarios ya cuadrados en los que sabemos que no se faltan objetos o demas
# en listas grandes tambien, y en inventarios que tambien sabemos que estan mal asi tenemos tanto comprobada la repuesta correcta y la mala, asegurando que no nos afectara en listas grandes