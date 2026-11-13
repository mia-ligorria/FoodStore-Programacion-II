
from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago


class Pedido(Base, Calculable):

    def __init__(
        self,
        usuario: Usuario,
        forma_pago: FormaPago
    ) -> None:
        super().__init__()

        self.__usuario = usuario
        self.__detalles: list[DetallePedido] = []
        self.__estado = Estado.PENDIENTE
        self.__forma_pago = forma_pago
        self.__fecha = date.today()
        self.__total: float = 0.0

    @property
    def usuario(self) -> Usuario:
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
    def fecha(self) -> date:
        return self.__fecha

    @property
    def total(self) -> float:
        return self.__total

    def agregar_detalle(
        self,
        cantidad: int,
        producto
    ) -> None:
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if not producto.disponible:
            raise ValueError("El producto no está disponible.")

        if producto.stock < cantidad:
            raise ValueError("No hay stock suficiente.")

        detalle_existente = self.buscar_detalle_por_producto(producto)

        if detalle_existente is not None:
            detalle_existente.incrementar_cantidad(cantidad)
        else:
            detalle = DetallePedido(
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
            self.__detalles.append(detalle)

        producto.stock -= cantidad
        self.calcular_total()

    def buscar_detalle_por_producto(
        self,
        producto
    ) -> DetallePedido | None:

        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle

        return None

    def eliminar_detalle_por_producto(self, producto) -> None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                self.__detalles.remove(detalle)
                producto.stock += detalle.cantidad
                self.calcular_total()
                return

    def cambiar_estado(self, nuevo_estado: Estado) -> None:

        if not isinstance(nuevo_estado, Estado):
            raise TypeError("El estado debe ser un valor válido.")

        transiciones_permitidas = {
            Estado.PENDIENTE: [
                Estado.CONFIRMADO,
                Estado.CANCELADO
            ],
            Estado.CONFIRMADO: [
                Estado.TERMINADO,
                Estado.CANCELADO
            ],
            Estado.TERMINADO: [],
            Estado.CANCELADO: []
        }

        if nuevo_estado not in transiciones_permitidas[self.__estado]:
            raise ValueError(
                f"No se puede cambiar de {self.__estado.name} "
                f"a {nuevo_estado.name}."
            )

        if nuevo_estado == Estado.CANCELADO:
            for detalle in self.__detalles:
                detalle.producto.stock += detalle.cantidad

        self.__estado = nuevo_estado

    def calcular_total(self) -> None:
        self.__total = sum(
            detalle.calcular_subtotal()
            for detalle in self.__detalles
        )

    def __str__(self) -> str:
        return (
            f"Pedido N° {self.id} | "
            f"Usuario: {self.__usuario.nombre} "
            f"{self.__usuario.apellido} | "
            f"Estado: {self.__estado.name} | "
            f"Total: ${self.__total:.2f}"
        )
