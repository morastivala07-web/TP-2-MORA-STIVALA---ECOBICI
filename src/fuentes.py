import csv
import json
from abc import ABC, abstractmethod


class FuenteDatos(ABC):
    @abstractmethod
    def cargar(self, ruta):
        pass


class FuenteCSV(FuenteDatos):
    def cargar(self, ruta):
        try:
            with open(
                ruta, encoding="utf-8-sig", newline=""
            ) as archivo:
                lector = csv.DictReader(archivo, strict=True)
                campos = lector.fieldnames

                if not campos:
                    raise ValueError("El CSV no tiene encabezados.")

                if any(not campo.strip() for campo in campos):
                    raise ValueError("El CSV tiene encabezados vacíos.")

                if len(campos) != len(set(campos)):
                    raise ValueError("El CSV tiene encabezados repetidos.")

                registros = []

                for fila in lector:
                    if None in fila or any(
                        valor is None for valor in fila.values()
                    ):
                        raise ValueError(
                            "Cantidad incorrecta de campos en la línea "
                            + str(lector.line_num)
                        )

                    registros.append(fila)

                return registros

        except csv.Error as error:
            raise ValueError(
                "El CSV está mal formado: " + str(error)
            ) from error


class FuenteJSON(FuenteDatos):
    def cargar(self, ruta):
        with open(ruta, encoding="utf-8-sig") as archivo:
            registros = json.load(archivo)

        if not isinstance(registros, list):
            raise ValueError("El JSON debe contener una lista.")

        if not all(isinstance(fila, dict) for fila in registros):
            raise ValueError("Cada registro JSON debe ser un objeto.")

        return registros