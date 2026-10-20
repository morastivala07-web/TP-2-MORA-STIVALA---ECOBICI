import csv
import json
from datetime import datetime, timedelta
from pathlib import Path


def main():
    carpeta = Path(__file__).resolve().parent.parent / "data"
    carpeta.mkdir(parents=True, exist_ok=True)

    estaciones = ["Estación A", "Estación B", "Estación C", "Estación D"]
    registros = []

    for numero in range(50):
        inicio = datetime(2026, 10, 1, 8) + timedelta(hours=numero * 3)
        fin = inicio + timedelta(minutes=15 + numero % 30)

        registros.append({
            "id_viaje": "V-" + str(numero + 1).zfill(3),
            "inicio": inicio.strftime("%Y-%m-%d %H:%M"),
            "fin": fin.strftime("%Y-%m-%d %H:%M"),
            "origen": estaciones[numero % 4],
            "destino": estaciones[(numero + 1) % 4]
        })

    # Un viaje aceptado tendrá espacios para probar la limpieza.
    registros[0]["origen"] = " Estación A "

    # Copia del primer viaje: debe rechazarse por identificador duplicado.
    registros.append(dict(registros[0]))

    registros.append({
        "id_viaje": "V-051",
        "inicio": "2026-02-30 10:00",
        "fin": "2026-03-01 10:30",
        "origen": "Estación A",
        "destino": "Estación B"
    })

    registros.append({
        "id_viaje": "V-052",
        "inicio": "2026-10-02 12:00",
        "fin": "2026-10-02 11:00",
        "origen": "Estación B",
        "destino": "Estación C"
    })

    registros.append({
        "id_viaje": "V-053",
        "inicio": "2026-10-02 12:00",
        "fin": "2026-10-02 12:30",
        "origen": "Estación C",
        "destino": ""
    })

    campos = ["id_viaje", "inicio", "fin", "origen", "destino"]

    with open(
        carpeta / "viajes.csv",
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)

    with open(
        carpeta / "viajes.json",
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=4)

    print("Se generaron 54 registros en CSV y JSON.")
    print("Esperados: 50 viajes válidos, 4 rechazos y 1 campo limpiado.")
    print("Período de demostración: del 2026-10-01 al 2026-10-07.")


if __name__ == "__main__":
    main()