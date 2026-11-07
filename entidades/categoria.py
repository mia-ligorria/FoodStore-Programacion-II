# ==================================================
# Clase Categoria
# Representa una categoría de productos.
# ==================================================

from entidades.base import Base

class Categoria(Base):
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()

        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser un texto.")
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        self.__nombre = nombre.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        if not isinstance(descripcion, str):
            raise TypeError("La descripción debe ser un texto.")
        if not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía.")

        self.__descripcion = descripcion.strip()

    def __str__(self) -> str:
        return f"Categoría: {self.nombre} - {self.descripcion}"