import sys
import unittest
from datetime import date
from pathlib import Path


PROYECTO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROYECTO / "src"))

from fuentes import FuenteCSV, FuenteJSON
from pipeline import (
    convertir_fecha,
    validar_recorridos,
    seleccionar_periodo,
    generar_balance
)


def crear_viaje(**cambios):
    viaje = {
        "id_viaje": "V-001",
        "inicio": "2026-10-01 23:50",
        "fin": "2026-10-02 00:20",
        "origen": "A",
        "destino": "B"
    }
    viaje.update(cambios)
    return viaje


class PruebasEcobici(unittest.TestCase):
    def test_viaje_normal(self):
        validos, rechazos, cambios = validar_recorridos(
            [crear_viaje()]
        )

        self.assertEqual(len(validos), 1)
        self.assertEqual(rechazos, [])
        self.assertEqual(cambios, [])

        self.assertEqual(generar_balance(validos), [
            {"estacion": "A", "salidas": 1, "llegadas": 0, "balance": -1},
            {"estacion": "B", "salidas": 0, "llegadas": 1, "balance": 1}
        ])

    def test_fechas_invalidas(self):
        for texto in ["2026-02-30 10:00", "01/10/2026 10:00"]:
            with self.subTest(fecha=texto):
                with self.assertRaises(ValueError):
                    convertir_fecha(texto)

    def test_rechazos(self):
        registros = [
            crear_viaje(),
            crear_viaje(),
            crear_viaje(id_viaje="V-002", destino=""),
            crear_viaje(
                id_viaje="V-003",
                fin="2026-10-01 20:00"
            )
        ]

        validos, rechazos, _ = validar_recorridos(registros)

        self.assertEqual(len(validos), 1)
        self.assertEqual(len(rechazos), 3)
        self.assertTrue(all(r["motivo"] for r in rechazos))
        self.assertEqual(
            sum(f["salidas"] for f in generar_balance(validos)),
            1
        )

    def test_limpieza(self):
        validos, rechazos, cambios = validar_recorridos(
            [crear_viaje(origen=" A ")]
        )

        self.assertEqual(validos[0]["origen"], "A")
        self.assertEqual(rechazos, [])
        self.assertEqual(len(cambios), 1)

    def test_periodo_por_inicio(self):
        validos, _, _ = validar_recorridos([crear_viaje()])

        seleccionados = seleccionar_periodo(
            validos, date(2026, 10, 1), date(2026, 10, 1)
        )
        self.assertEqual(len(seleccionados), 1)

        self.assertEqual(
            seleccionar_periodo(
                validos, date(2026, 10, 2), date(2026, 10, 2)
            ),
            []
        )

        with self.assertRaises(ValueError):
            seleccionar_periodo(
                validos, date(2026, 10, 2), date(2026, 10, 1)
            )

    def test_periodo_sin_viajes(self):
        self.assertEqual(generar_balance([]), [])

    def test_regreso_a_misma_estacion(self):
        validos, _, _ = validar_recorridos(
            [crear_viaje(destino="A")]
        )

        self.assertEqual(generar_balance(validos), [
            {"estacion": "A", "salidas": 1, "llegadas": 1, "balance": 0}
        ])

    def test_equivalencia_y_conservacion(self):
        csv = FuenteCSV().cargar(PROYECTO / "data" / "viajes.csv")
        json = FuenteJSON().cargar(PROYECTO / "data" / "viajes.json")

        self.assertEqual(csv, json)

        validos, rechazos, cambios = validar_recorridos(csv)
        validos_json, rechazos_json, cambios_json = validar_recorridos(json)

        self.assertEqual(len(validos), 50)
        self.assertEqual(len(rechazos), 4)
        self.assertEqual(len(cambios), 1)
        self.assertEqual(rechazos, rechazos_json)
        self.assertEqual(cambios, cambios_json)

        reporte = generar_balance(validos)
        self.assertEqual(reporte, generar_balance(validos_json))
        self.assertEqual(sum(f["salidas"] for f in reporte), 50)
        self.assertEqual(sum(f["llegadas"] for f in reporte), 50)
        self.assertEqual(sum(f["balance"] for f in reporte), 0)


if __name__ == "__main__":
    unittest.main()