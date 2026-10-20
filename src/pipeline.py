import re
from datetime import datetime

from modelos import BalanceEstacion


CAMPOS = {"id_viaje", "inicio", "fin", "origen", "destino"}


def convertir_fecha(texto):
    if not isinstance(texto, str):
        raise ValueError("La fecha debe ser texto.")

    if not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}",
        texto
    ):
        raise ValueError("Usá el formato AAAA-MM-DD HH:MM.")

    try:
        return datetime.strptime(texto, "%Y-%m-%d %H:%M")
    except ValueError as error:
        raise ValueError("La fecha o la hora no existe.") from error


def validar_recorridos(registros):
    validos = []
    rechazos = []
    cambios = []
    identificadores = set()

    for posicion, original in enumerate(registros, start=1):
        try:
            if not CAMPOS.issubset(original):
                raise ValueError("Faltan campos obligatorios.")

            if any(
                not isinstance(original[campo], str)
                for campo in CAMPOS
            ):
                raise ValueError("Todos los campos deben ser texto.")

            fila = {
                campo: original[campo].strip()
                for campo in sorted(CAMPOS)
            }

            if any(not valor for valor in fila.values()):
                raise ValueError("Hay campos obligatorios vacíos.")

            if fila["id_viaje"] in identificadores:
                raise ValueError("Identificador de viaje duplicado.")

            inicio = convertir_fecha(fila["inicio"])
            fin = convertir_fecha(fila["fin"])

            if fin <= inicio:
                raise ValueError("El fin debe ser posterior al inicio.")

            identificadores.add(fila["id_viaje"])

            for campo in sorted(CAMPOS):
                if original[campo] != fila[campo]:
                    cambios.append({
                        "registro": posicion,
                        "campo": campo,
                        "original": original[campo],
                        "limpio": fila[campo]
                    })

            fila["inicio"] = inicio
            fila["fin"] = fin
            validos.append(fila)

        except ValueError as error:
            rechazos.append({
                "registro": posicion,
                "motivo": str(error),
                "datos": dict(original)
            })

    return validos, rechazos, cambios


def seleccionar_periodo(viajes, desde, hasta):
    if desde > hasta:
        raise ValueError("La fecha inicial no puede superar la final.")

    return [
        viaje
        for viaje in viajes
        if desde <= viaje["inicio"].date() <= hasta
    ]


def registrar_movimientos(viajes):
    estaciones = {}

    for viaje in viajes:
        origen = viaje["origen"]
        destino = viaje["destino"]

        if origen not in estaciones:
            estaciones[origen] = BalanceEstacion(origen)

        if destino not in estaciones:
            estaciones[destino] = BalanceEstacion(destino)

        estaciones[origen].registrar_salida()
        estaciones[destino].registrar_llegada()

    return estaciones


def generar_balance(viajes):
    estaciones = registrar_movimientos(viajes)

    reporte = [
        estaciones[nombre].como_diccionario()
        for nombre in sorted(estaciones)
    ]

    total_salidas = sum(fila["salidas"] for fila in reporte)
    total_llegadas = sum(fila["llegadas"] for fila in reporte)
    total_balance = sum(fila["balance"] for fila in reporte)

    if (
        total_salidas != len(viajes)
        or total_llegadas != len(viajes)
        or total_balance != 0
    ):
        raise ValueError("Los conteos del reporte son inconsistentes.")

    return reporte