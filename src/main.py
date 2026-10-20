from pathlib import Path

from fuentes import FuenteCSV, FuenteJSON
from pipeline import (
    convertir_fecha,
    validar_recorridos,
    seleccionar_periodo,
    generar_balance
)
from exportacion import guardar_resultados


def main():
    proyecto = Path(__file__).resolve().parent.parent

    try:
        formato = input("Formato de entrada (csv/json): ").strip().lower()

        if formato == "csv":
            fuente = FuenteCSV()
        elif formato == "json":
            fuente = FuenteJSON()
        else:
            raise ValueError("Elegí csv o json.")

        registros = fuente.cargar(
            proyecto / "data" / ("viajes." + formato)
        )

        if not registros:
            raise ValueError("El archivo de viajes está vacío.")

        validos, rechazos, cambios = validar_recorridos(registros)

        print("Registros leídos:", len(registros))
        print("Viajes válidos:", len(validos))
        print("Registros rechazados:", len(rechazos))
        print("Campos limpiados:", len(cambios))

        texto_desde = input("Fecha inicial (AAAA-MM-DD): ").strip()
        texto_hasta = input("Fecha final (AAAA-MM-DD): ").strip()

        desde = convertir_fecha(texto_desde + " 00:00").date()
        hasta = convertir_fecha(texto_hasta + " 00:00").date()

        seleccionados = seleccionar_periodo(validos, desde, hasta)
        reporte = generar_balance(seleccionados)

        guardar_resultados(
            proyecto / "outputs",
            reporte,
            rechazos,
            cambios
        )

        print("\nViajes seleccionados:", len(seleccionados))

        if not seleccionados:
            print("No hay viajes válidos iniciados en ese período.")
        else:
            print("\nEstación | Salidas | Llegadas | Balance")

            for fila in reporte:
                print(
                    fila["estacion"],
                    "|", fila["salidas"],
                    "|", fila["llegadas"],
                    "|", fila["balance"]
                )

        print(
            "\nSuma de balances:",
            sum(fila["balance"] for fila in reporte)
        )
        print("Archivos guardados en:", proyecto / "outputs")

    except (OSError, UnicodeError, ValueError) as error:
        print("No se pudo completar el reporte:", error)


if __name__ == "__main__":
    main()