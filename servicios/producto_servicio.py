# ==================================================
# Clase ProductoServicio
# Administra la colección de productos y sus operaciones.
# ==================================================

from entidades.producto import Producto
from entidades.categoria import Categoria
from servicios.categoria_servicio import CategoriaServicio
from excepciones import EntidadNoEncontradaError


class ProductoServicio:
    def __init__(self, categoria_servicio: CategoriaServicio) -> None:
        self.__productos: list[Producto] = []
        self.__categoria_servicio: CategoriaServicio = categoria_servicio


    def buscar_por_id(self, id: int) -> Producto | None:
        for producto in self.__productos:
            if producto.id == id:
                return producto
        return None


    def listar(self) -> list[Producto]:
        return [producto for producto in self.__productos if not producto.eliminado]


    def listar_disponibles(self) -> list[Producto]:
        return [producto for producto in self.listar() if producto.disponible and producto.stock>0]


    def agregar(self, nvo_producto: Producto) -> None:
        if not isinstance(nvo_producto, Producto):
            raise TypeError("Se debe agregar un objeto de tipo Producto.")

        categoria = self.__categoria_servicio.buscar_por_id(nvo_producto.categoria.id)
        if categoria is None or categoria.eliminado:
            raise EntidadNoEncontradaError(f"No existe una categoría activa con el ID {nvo_producto.categoria.id}.")

        self.__productos.append(nvo_producto)


    def editar(
        self,
        id: int,
        nvo_nombre: str,
        nvo_precio: float,
        nva_descripcion: str,
        nvo_stock: int,
        nva_imagen: str,
        nva_disponible: bool,
        nva_categoria: Categoria
    ) -> None:

        producto = self.buscar_por_id(id)

        if producto is None or producto.eliminado:
            raise EntidadNoEncontradaError(f"No existe un producto activo con el ID {id}.")
        if not isinstance(nva_categoria, Categoria):
            raise TypeError("La categoría debe ser un objeto de tipo Categoria.")

        categoria = self.__categoria_servicio.buscar_por_id(nva_categoria.id)

        if categoria is None or categoria.eliminado:
            raise EntidadNoEncontradaError("La categoría no existe o está eliminada.")

        producto.nombre = nvo_nombre
        producto.precio = nvo_precio
        producto.descripcion = nva_descripcion
        producto.stock = nvo_stock
        producto.imagen = nva_imagen
        producto.disponible = nva_disponible
        producto.categoria = categoria


    def eliminar(self, id:int) -> None:
        producto = self.buscar_por_id(id)
        if producto is None or producto.eliminado:
            raise EntidadNoEncontradaError(f"No existe un producto activo con el ID {id}.")
        producto.eliminado = True


    def contar_activos_x_categoria(self, categoria: Categoria) -> int:
        contador = 0
        for producto in self.__productos:
            if producto.categoria == categoria and not producto.eliminado:
                contador += 1
        return contador

