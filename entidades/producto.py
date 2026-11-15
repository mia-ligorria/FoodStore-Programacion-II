# ==================================================
# Clase Producto
# Representa un producto del catálogo.
# ==================================================

from entidades.base import Base
from entidades.categoria import Categoria
from excepciones import DatoInvalidoError, PrecioInvalidoError

class Producto(Base):

    """
    Utilizamos propiedades y setters para encapsular los atributos y
    controlar su modificación mediante validaciones.
    Los setters permiten mantener la integridad de los datos, 
    evitando que se asignen valores inválidos al crear el producto
    como al modificar sus atributos más adelante.
    """

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria
    ) -> None:
        super().__init__()

        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria


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
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, precio: float) -> None:
        if not isinstance(precio, (int,float)) or isinstance(precio, bool):
            raise TypeError("El precio debe ser un número.")
        if precio < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo.")

        self.__precio = precio


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
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, stock: int) -> None:
        if not isinstance(stock, int) or isinstance(stock, bool):
            raise TypeError("El stock debe ser un número entero.")
        if stock < 0:
            raise DatoInvalidoError("El stock no puede ser negativo.")

        self.__stock = stock


    @property
    def imagen(self) -> str:
        return self.__imagen
    
    @imagen.setter
    def imagen(self, imagen: str) -> None:
        if not isinstance(imagen, str):
            raise TypeError("La imagen debe ser un texto.")
        if not imagen.strip():
            raise DatoInvalidoError("La imagen no puede estar vacía.")

        self.__imagen = imagen.strip()


    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, disponible: bool) -> None:
        if not isinstance(disponible, bool):
            raise TypeError("La disponibilidad debe ser un valor booleano.")

        self.__disponible = disponible


    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria: Categoria) -> None:
        """
        Se recibe una categoría existente para establecer una relación
        de agregación, sin crear ni administrar la categoría desde Producto.
        """
        if not isinstance(categoria, Categoria):
            raise TypeError("La categoría debe ser un objeto de tipo Categoria.")

        self.__categoria = categoria


    def __str__(self) -> str:
        return (
            f"Producto: {self.nombre}\n"
            f"Precio: ${self.precio:.2f}\n"
            f"Descripción: {self.descripcion}\n"
            f"Stock: {self.stock}\n"
            f"Imagen: {self.imagen}\n"
            f"Disponible: {self.disponible}\n"
            f"Categoría: {self.categoria.nombre}"
        )