from datetime import datetime

from entidades.base import Base
from entidades.calculable import Calculable
from enums.estado import Estado
from enums.forma_pago import FormaPago
from entidades.detalle_pedido import DetallePedido


class Pedido(Base, Calculable):

    def __init__(
        self,
        usuario,
        forma_pago: FormaPago
    ) -> None:
        super().__init__()

        self.__usuario = usuario
        self.__detalles: list[DetallePedido] = []
        self.__estado = Estado.PENDIENTE
        self.__forma_pago = forma_pago
        self.__fecha = datetime.now()

    @property
    def usuario(self):
        return self.__usuario

    @property
    def detalles(self) -> list[DetallePedido]:
        return self.__detalles.copy()

    @property
    def estado(self) -> Estado:
        return self.__estado

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    def agregar_detalle(self, detalle: DetallePedido) -> None:
        self.__detalles.append(detalle)

    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        self.__estado = nuevo_estado

    def calcular_total(self) -> float:
        return sum(
            detalle.calcular_subtotal()
            for detalle in self.__detalles
        )

    def __str__(self) -> str:
        return (
            f"Pedido N° {self.id} | "
            f"Usuario: {self.__usuario.nombre} "
            f"{self.__usuario.apellido} | "
            f"Estado: {self.__estado.name} | "
            f"Total: ${self.calcular_total():.2f}"
        )