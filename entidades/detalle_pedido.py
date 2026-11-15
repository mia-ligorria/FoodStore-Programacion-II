# ==================================================
# Clase DetallePedido
# Representa un producto y su cantidad dentro de un pedido.
# ==================================================

from entidades.base import Base
from entidades.producto import Producto
from excepciones import DatoInvalidoError, PrecioInvalidoError


class DetallePedido(Base):
    def __init__(
        self,
        producto: Producto,
        cantidad: int,
        precio_unitario: float
    ) -> None:
        if not isinstance(producto, Producto):
            raise TypeError("El producto debe ser un objeto de tipo Producto.")

        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise DatoInvalidoError(
                "La cantidad debe ser mayor que cero."
            )

        if (
            not isinstance(precio_unitario, (int, float))
            or isinstance(precio_unitario, bool)
        ):
            raise TypeError("El precio unitario debe ser numérico.")

        if precio_unitario < 0:
            raise PrecioInvalidoError(
                "El precio unitario no puede ser negativo."
            )

        super().__init__()

        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio_unitario = float(precio_unitario)

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def precio_unitario(self) -> float:
        return self.__precio_unitario

    @property
    def subtotal(self) -> float:
        return self.calcular_subtotal()

    def calcular_subtotal(self) -> float:
        return self.__cantidad * self.__precio_unitario

    def incrementar_cantidad(self, cantidad: int) -> None:
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise DatoInvalidoError(
                "La cantidad debe ser mayor que cero."
            )

        self.__cantidad += cantidad

    def __str__(self) -> str:
        return (
            f"Producto: {self.__producto} | "
            f"Cantidad: {self.__cantidad} | "
            f"Precio unitario: ${self.__precio_unitario:.2f} | "
            f"Subtotal: ${self.subtotal:.2f}"
        )