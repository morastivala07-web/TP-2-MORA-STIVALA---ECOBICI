import csv
import json
from pathlib import Path


def guardar_csv(ruta, campos, registros):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(
        ruta, "w", encoding="utf-8-sig", newline=""
    ) as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)


def guardar_resultados(carpeta, reporte, rechazos, cambios):
    carpeta = Path(carpeta)

    guardar_csv(
        carpeta / "reporte_estaciones.csv",
        ["estacion", "salidas", "llegadas", "balance"],
        reporte
    )

    rechazos_exportables = [
        {
            "registro": rechazo["registro"],
            "motivo": rechazo["motivo"],
            "datos": json.dumps(
                rechazo["datos"], ensure_ascii=False
            )
        }
        for rechazo in rechazos
    ]

    guardar_csv(
        carpeta / "rechazos.csv",
        ["registro", "motivo", "datos"],
        rechazos_exportables
    )

    guardar_csv(
        carpeta / "limpieza.csv",
        ["registro", "campo", "original", "limpio"],
        cambios
    )