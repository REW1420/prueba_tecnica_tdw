from collections import defaultdict

orders = [
 {"cliente":"Ana","estado":"COMPLETADA","monto":120},
 {"cliente":"Luis","estado":"PENDIENTE","monto":50},
 {"cliente":"Ana","estado":"COMPLETADA","monto":80},
 {"cliente":"Pedro","estado":"COMPLETADA","monto":200}
]

def resumen_por_cliente(orders):
    acumulado = defaultdict(lambda: {"total_comprado": 0, "cantidad_ordenes": 0})

    for orden in orders:
        if orden.get("estado") != "COMPLETADA":
            continue

        cliente = orden["cliente"]
        acumulado[cliente]["total_comprado"] += orden["monto"]
        acumulado[cliente]["cantidad_ordenes"] += 1

    return {
        cliente: {
            **datos,
            "promedio_compra": datos["total_comprado"] / datos["cantidad_ordenes"],
        }
        for cliente, datos in acumulado.items()
    }


print(resumen_por_cliente(orders))
