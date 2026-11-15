# ==================================================
# Clase Calculable
# Interfaz que define el cálculo del total de un pedido.
# ==================================================

from abc import ABC, abstractmethod

class Calculable(ABC):

    @abstractmethod
    def calcular_total(self) -> None:
        pass