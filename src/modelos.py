from dataclasses import dataclass


@dataclass
class BalanceEstacion:
    estacion: str
    salidas: int = 0
    llegadas: int = 0

    def registrar_salida(self):
        self.salidas += 1

    def registrar_llegada(self):
        self.llegadas += 1

    def balance(self):
        return self.llegadas - self.salidas

    def como_diccionario(self):
        return {
            "estacion": self.estacion,
            "salidas": self.salidas,
            "llegadas": self.llegadas,
            "balance": self.balance()
        }