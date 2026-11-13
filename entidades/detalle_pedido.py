from entidades.base import Base
from excepciones.dato_invalido_error import DatoInvalidoError



class DetallePedido(Base):

    def __init__(
        self,
        producto,
        cantidad: int,
        precio_unitario: float
    ) -> None:

        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise DatoInvalidoError(
                "La cantidad debe ser mayor que cero."
            )

        if not isinstance(precio_unitario, (int, float)) or isinstance(precio_unitario, bool):
            raise TypeError("El precio unitario debe ser numérico.")

        if precio_unitario < 0:
            raise DatoInvalidoError(
                "El precio unitario no puede ser negativo."
            )

        super().__init__()

        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio_unitario = float(precio_unitario)

    @property
    def producto(self):
        return self.__producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def precio_unitario(self) -> float:
        return self.__precio_unitario

    def calcular_subtotal(self) -> float:
        return self.__cantidad * self.__precio_unitario

    def __str__(self) -> str:
        return (
            f"Producto: {self.__producto} | "
            f"Cantidad: {self.__cantidad} | "
            f"Precio unitario: ${self.__precio_unitario:.2f} | "
            f"Subtotal: ${self.calcular_subtotal():.2f}"
        )
    

    def incrementar_cantidad(self, cantidad: int) -> None:
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un número entero.")

        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor que cero.")

        self.__cantidad += cantidad