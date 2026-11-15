# ==================================================
# Clase CategoriaServicio
# Administra la colección de categorías y sus operaciones
# ==================================================

from entidades.categoria import Categoria
from excepciones import EntidadNoEncontradaError, DuplicadoError, OperacionNoPermitidaError, DatoInvalidoError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from servicios.producto_servicio import ProductoServicio

class CategoriaServicio:
    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []


# ==================================================
# Métodos: 
# ==================================================
    def buscar_por_id(self, id: int) -> Categoria | None:
        for categoria in self.__categorias:
            if categoria.id == id:
                return categoria
        return None


    def listar(self) -> list[Categoria]:
        return [categoria for categoria in self.__categorias if not categoria.eliminado]


    def agregar(self, nva_categoria: Categoria) -> None:
        if not isinstance(nva_categoria,Categoria):
            raise TypeError("Se debe agregar un objeto de tipo Categoria")
        if nva_categoria.eliminado:
            raise DatoInvalidoError("No se puede agregar una categoría eliminada.")
        for categoria in self.__categorias:
            if (
                categoria.nombre.strip().lower() == nva_categoria.nombre.strip().lower()
                and not categoria.eliminado
            ):
                raise DuplicadoError("Ya existe una categoría con ese nombre.")
        self.__categorias.append(nva_categoria)


    def editar(self, id: int, nvo_nombre: str, nva_descripcion: str) -> None:
        categoria = self.buscar_por_id(id)
        if categoria is None or categoria.eliminado:
            raise EntidadNoEncontradaError("Categoría no encontrada.")
        if not isinstance(nvo_nombre, str):
            raise TypeError("El nombre debe ser un texto.")
        if not nvo_nombre.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        if not isinstance(nva_descripcion, str):
            raise TypeError("La descripción debe ser un texto.")
        if not nva_descripcion.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía.")

        for cat_existente in self.__categorias:
            if (
                cat_existente.nombre.lower() == nvo_nombre.strip().lower()
                and not cat_existente.eliminado
                and cat_existente.id != categoria.id
            ):
                raise DuplicadoError("Ya existe una categoría con ese nombre.")

        categoria.nombre = nvo_nombre
        categoria.descripcion = nva_descripcion


    def eliminar(self, id: int, producto_servicio:"ProductoServicio") -> None:
        categoria = self.buscar_por_id(id)

        if categoria is None or categoria.eliminado:
            raise EntidadNoEncontradaError("No se encontró una categoría con ese ID.")

        cantidad = producto_servicio.contar_activos_x_categoria(categoria)
        if cantidad>0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría. "
                f"Tiene {cantidad} productos activos."
            )
        categoria.eliminado = True