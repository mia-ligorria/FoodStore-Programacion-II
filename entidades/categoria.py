# ==================================================
# Clase Categoria
# Representa una categoría de productos.
# ==================================================
from typing import TYPE_CHECKING

from entidades.base import Base
from excepciones import DatoInvalidoError

if TYPE_CHECKING:
    from entidades.producto import Producto

class Categoria(Base):
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()

        self.nombre = nombre
        self.descripcion = descripcion
        self.__productos: list["Producto"] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser un texto.")
        if not nombre.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")

        self.__nombre = nombre.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        if not isinstance(descripcion, str):
            raise TypeError("La descripción debe ser un texto.")
        if not descripcion.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía.")

        self.__descripcion = descripcion.strip()

    @property
    def productos(self) -> list["Producto"]:
        return self.__productos.copy()

    def agregar_producto(self, producto: "Producto") -> None:
        from entidades.producto import Producto
        if not isinstance(producto, Producto):
            raise TypeError("El producto debe ser una instancia de Producto.")
        if self.eliminado:
            raise DatoInvalidoError(
                "No se pueden agregar productos a una categoría eliminada."
            )
        if producto.eliminado:
            raise DatoInvalidoError(
                "No se puede agregar un producto eliminado."
            )
        if producto.categoria != self:
            raise DatoInvalidoError(
                "El producto pertenece a otra categoría."
            )
        if producto in self.__productos:
            raise DatoInvalidoError(
                "El producto ya pertenece a esta categoría."
            )
        self.__productos.append(producto)

    def quitar_producto(self, producto: "Producto") -> None:
        from entidades.producto import Producto
        if not isinstance(producto, Producto):
            raise TypeError("El producto debe ser una instancia de Producto.")
        if producto not in self.__productos:
            raise DatoInvalidoError(
                "El producto no pertenece a esta categoría."
            )
        self.__productos.remove(producto)

    def contar_productos_activos(self) -> int:
        cantidad: int = 0
        for producto in self.__productos:
            if not producto.eliminado:
                cantidad += 1
        return cantidad

    def __str__(self) -> str:
        return f"Categoría: {self.nombre} - {self.descripcion}"