# ==================================================
# MENU ADMINISTRADOR - FOOD STORE
# Programación II - UTN FRM
# ==================================================

import questionary
from entidades.usuario import Usuario
from entidades.categoria import Categoria
from entidades.producto import Producto
from consola.menu import Menu
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from excepciones import FoodStoreError
from consola.utilidades_consola import (
    limpiar_consola,
    mostrar_titulo,
    mostrar_menu,
    mostrar_exito,
    mostrar_error,
    mostrar_aviso,
    pausar
)

class MenuAdministrador(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio
    ) -> None:
        super().__init__(usuario)
        self.__categoria_servicio: CategoriaServicio = categoria_servicio
        self.__producto_servicio: ProductoServicio = producto_servicio


# MENU PRINCIPAL

    def mostrar(self) -> bool:
        while True:
            limpiar_consola()
            mostrar_titulo(
                f"FOOD STORE - ADMINISTRADOR "
                f"({self._usuario.nombre} {self._usuario.apellido})"
            )
            opciones: list[str] = [
                "Categorías",
                "Productos",
                "Usuarios",
                "Pedidos",
                "Cerrar sesión",
                "Salir"
            ]
            seleccion = mostrar_menu(
                "Seleccioná una opción:",
                opciones
            )
            match seleccion:
                case "Categorías":
                    self._menu_categorias()
                case "Productos":
                    self._menu_productos()
                case "Usuarios":
                    self._menu_usuarios()
                case "Pedidos":
                    self._menu_pedidos()
                case "Cerrar sesión":
                    return True
                case "Salir":
                    return False
                case None:
                    return True


# GESTIÓN DE CATEGORÍAS

    def _menu_categorias(self) -> None:
        while True:
            limpiar_consola()
            mostrar_titulo("GESTIÓN DE CATEGORÍAS")
            opciones: list[str] = [
                "Listar",
                "Crear",
                "Editar",
                "Eliminar",
                "Volver"
            ]
            seleccion = mostrar_menu(
                "Seleccioná una operación:",
                opciones
            )
            match seleccion:
                case "Listar":
                    self._listar_categorias()
                case "Crear":
                    self._crear_categoria()
                case "Editar":
                    self._editar_categoria()
                case "Eliminar":
                    self._eliminar_categoria()
                case None | "Volver":
                    break

    def _listar_categorias(self) -> None:
        limpiar_consola()
        mostrar_titulo("LISTADO DE CATEGORÍAS")
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            mostrar_aviso("No hay categorías registradas.")
        else:
            self._listar_categorias_sin_pausar(categorias)
        pausar()

    def _crear_categoria(self) -> None:
        limpiar_consola()
        mostrar_titulo("CREAR CATEGORÍA")
        nombre = questionary.text(
            "Ingresá el nombre:"
        ).ask()
        if nombre is None:
            return
        descripcion = questionary.text(
            "Ingresá la descripción:"
        ).ask()
        if descripcion is None:
            return

        try:
            categoria = Categoria(nombre, descripcion)
            self.__categoria_servicio.agregar(categoria)
            mostrar_exito(
                f"Categoría creada correctamente. ID: {categoria.id}"
            )
        except (FoodStoreError, TypeError, ValueError) as error:
            mostrar_error(str(error))
        pausar()

    def _editar_categoria(self) -> None:
        limpiar_consola()
        mostrar_titulo("EDITAR CATEGORÍA")
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            mostrar_aviso("No hay categorías para editar.")
            pausar()
            return

        self._listar_categorias_sin_pausar(categorias)
        id_ingresado = questionary.text(
            "Ingresá el ID de la categoría:"
        ).ask()
        if id_ingresado is None:
            return

        try:
            id_categoria = int(id_ingresado)
            categoria = self.__categoria_servicio.buscar_por_id(
                id_categoria
            )
            if categoria is None or categoria.eliminado:
                mostrar_error("No se encontró una categoría con ese ID.")
                pausar()
                return
            nuevo_nombre = questionary.text(
                f"Nuevo nombre (actual: {categoria.nombre}):"
            ).ask()
            if nuevo_nombre is None:
                return
            nueva_descripcion = questionary.text(
                f"Nueva descripción (actual: {categoria.descripcion}):"
            ).ask()

            if nueva_descripcion is None:
                return
            if nuevo_nombre.strip() == "":
                nuevo_nombre = categoria.nombre
            if nueva_descripcion.strip() == "":
                nueva_descripcion = categoria.descripcion
            self.__categoria_servicio.editar(
                id_categoria,
                nuevo_nombre,
                nueva_descripcion
            )
            mostrar_exito("Categoría actualizada correctamente.")
        except (FoodStoreError, TypeError, ValueError) as error:
            mostrar_error(str(error))
        pausar()

    def _eliminar_categoria(self) -> None:
        limpiar_consola()
        mostrar_titulo("ELIMINAR CATEGORÍA")
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            mostrar_aviso("No hay categorías para eliminar.")
            pausar()
            return
        self._listar_categorias_sin_pausar(categorias)

        id_ingresado = questionary.text(
            "Ingresá el ID de la categoría:"
        ).ask()
        if id_ingresado is None:
            return

        try:
            id_categoria = int(id_ingresado)
            categoria = self.__categoria_servicio.buscar_por_id(
                id_categoria
            )
            if categoria is None or categoria.eliminado:
                mostrar_error("No se encontró una categoría con ese ID.")
                pausar()
                return
            confirmar = questionary.confirm(
                f"¿Querés eliminar la categoría '{categoria.nombre}'?"
            ).ask()

            if confirmar is not True:
                mostrar_aviso("Operación cancelada.")
                pausar()
                return
            self.__categoria_servicio.eliminar(
                id_categoria,
                self.__producto_servicio
            )
            mostrar_exito("Categoría eliminada correctamente.")
        except (FoodStoreError, TypeError, ValueError) as error:
            mostrar_error(str(error))
        pausar()

    def _listar_categorias_sin_pausar(
        self,
        categorias: list[Categoria]
    ) -> None:

        for categoria in categorias:
            print(
                f"\nID: {categoria.id}"
                f"\nNombre: {categoria.nombre}"
                f"\nDescripción: {categoria.descripcion}"
            )
            print("-" * 50)


# GESTIÓN DE PRODUCTOS

    def _menu_productos(self) -> None:
        while True:
            limpiar_consola()
            mostrar_titulo("GESTIÓN DE PRODUCTOS")
            opciones: list[str] = [
                "Listar",
                "Crear",
                "Editar",
                "Eliminar",
                "Volver"
            ]

            seleccion = mostrar_menu(
                "Seleccioná una operación:",
                opciones
            )

            match seleccion:
                case "Listar":
                    self._listar_productos()
                case "Crear":
                    self._crear_producto()
                case "Editar":
                    self._editar_producto()
                case "Eliminar":
                    self._eliminar_producto()
                case None | "Volver":
                    break

    def _listar_productos(self) -> None:
        limpiar_consola()
        mostrar_titulo("LISTADO DE PRODUCTOS")
        productos = self.__producto_servicio.listar()

        if not productos:
            mostrar_aviso("No hay productos registrados.")
        else:
            self._mostrar_productos_sin_pausar(productos)

        pausar()

    def _mostrar_productos_sin_pausar(
        self,
        productos: list[Producto]
    ) -> None:

        for producto in productos:
            print(
                f"\nID: {producto.id}"
                f"\nNombre: {producto.nombre}"
                f"\nDescripción: {producto.descripcion}"
                f"\nPrecio: ${producto.precio:.2f}"
                f"\nStock: {producto.stock}"
                f"\nImagen: {producto.imagen}"
                f"\nDisponible: {'Sí' if producto.disponible else 'No'}"
                f"\nCategoría: {producto.categoria.nombre}"
            )
            print("-" * 50)

    def _crear_producto(self) -> None:
        limpiar_consola()
        mostrar_titulo("CREAR PRODUCTO")

        nombre = questionary.text(
            "Ingresá el nombre:"
        ).ask()

        if nombre is None:
            return
        descripcion = questionary.text(
            "Ingresá la descripción:"
        ).ask()

        if descripcion is None:
            return
        precio = questionary.text(
            "Ingresá el precio:"
        ).ask()

        if precio is None:
            return
        stock = questionary.text(
            "Ingresá el stock:"
        ).ask()

        if stock is None:
            return
        imagen = questionary.text(
            "Ingresá la ruta o URL de la imagen:"
        ).ask()

        if imagen is None:
            return
        disponible = questionary.confirm(
            "¿El producto está disponible?",
            default=True
        ).ask()

        if disponible is None:
            return
        categoria = self._seleccionar_categoria()

        if categoria is None:
            return
        try:
            nuevo_producto = Producto(
                nombre=nombre,
                precio=float(precio.replace(",", ".")),
                descripcion=descripcion,
                stock=int(stock),
                imagen=imagen,
                disponible=disponible,
                categoria=categoria
            )
            self.__producto_servicio.agregar(nuevo_producto)

            mostrar_exito(
                f"Producto creado correctamente. ID: {nuevo_producto.id}"
            )
        except (FoodStoreError, TypeError, ValueError) as error:
            mostrar_error(str(error))

        pausar()

    def _editar_producto(self) -> None:
        limpiar_consola()
        mostrar_titulo("EDITAR PRODUCTO")
        productos = self.__producto_servicio.listar()

        if not productos:
            mostrar_aviso("No hay productos para editar.")
            pausar()
            return

        self._mostrar_productos_sin_pausar(productos)

        id_ingresado = questionary.text(
            "Ingresá el ID del producto:"
        ).ask()

        if id_ingresado is None:
            return

        try:
            id_producto = int(id_ingresado)
            producto = self.__producto_servicio.buscar_por_id(
                id_producto
            )

            if producto is None or producto.eliminado:
                mostrar_error("No se encontró un producto con ese ID.")
                pausar()
                return

            nuevo_nombre = questionary.text(
                f"Nombre (actual: {producto.nombre}):"
            ).ask()

            if nuevo_nombre is None:
                return
            nueva_descripcion = questionary.text(
                f"Descripción (actual: {producto.descripcion}):"
            ).ask()

            if nueva_descripcion is None:
                return
            nuevo_precio = questionary.text(
                f"Precio (actual: {producto.precio}):"
            ).ask()

            if nuevo_precio is None:
                return
            nuevo_stock = questionary.text(
                f"Stock (actual: {producto.stock}):"
            ).ask()

            if nuevo_stock is None:
                return
            nueva_imagen = questionary.text(
                f"Imagen (actual: {producto.imagen}):"
            ).ask()

            if nueva_imagen is None:
                return
            nueva_disponibilidad = questionary.confirm(
                "¿El producto está disponible?",
                default=producto.disponible
            ).ask()

            if nueva_disponibilidad is None:
                return
            nueva_categoria = self._seleccionar_categoria(
                producto.categoria
            )

            if nueva_categoria is None:
                return
            if nuevo_nombre.strip() == "":
                nuevo_nombre = producto.nombre
            if nueva_descripcion.strip() == "":
                nueva_descripcion = producto.descripcion
            if nuevo_precio.strip() == "":
                nuevo_precio = str(producto.precio)
            if nuevo_stock.strip() == "":
                nuevo_stock = str(producto.stock)
            if nueva_imagen.strip() == "":
                nueva_imagen = producto.imagen

            self.__producto_servicio.editar(
                id_producto,
                nuevo_nombre,
                float(nuevo_precio.replace(",", ".")),
                nueva_descripcion,
                int(nuevo_stock),
                nueva_imagen,
                nueva_disponibilidad,
                nueva_categoria
            )

            mostrar_exito("Producto actualizado correctamente.")
        except (FoodStoreError, TypeError, ValueError) as error:
            mostrar_error(str(error))

        pausar()

    def _eliminar_producto(self) -> None:
        limpiar_consola()
        mostrar_titulo("ELIMINAR PRODUCTO")

        productos = self.__producto_servicio.listar()

        if not productos:
            mostrar_aviso("No hay productos para eliminar.")
            pausar()
            return
        self._mostrar_productos_sin_pausar(productos)

        id_ingresado = questionary.text(
            "Ingresá el ID del producto:"
        ).ask()

        if id_ingresado is None:
            return
        try:
            id_producto = int(id_ingresado)
            producto = self.__producto_servicio.buscar_por_id(
                id_producto
            )
            if producto is None or producto.eliminado:
                mostrar_error("No se encontró un producto con ese ID.")
                pausar()
                return
            confirmar = questionary.confirm(
                f"¿Querés eliminar el producto '{producto.nombre}'?"
            ).ask()

            if confirmar is not True:
                mostrar_aviso("Operación cancelada.")
                pausar()
                return

            self.__producto_servicio.eliminar(id_producto)
            mostrar_exito("Producto eliminado correctamente.")
        except (FoodStoreError, TypeError, ValueError) as error:
            mostrar_error(str(error))

        pausar()


# SELECCIÓN DE CATEGORÍA

    def _seleccionar_categoria(
        self,
        categoria_actual: Categoria | None = None
    ) -> Categoria | None:

        categorias = self.__categoria_servicio.listar()

        if not categorias:
            mostrar_aviso("No hay categorías activas registradas.")
            pausar()
            return None
        opciones: list[str] = []
        categoria_actual_activa = False

        if categoria_actual is not None:
            for categoria in categorias:
                if categoria.id == categoria_actual.id:
                    categoria_actual_activa = True
                    break
        if categoria_actual_activa:
            opciones.append("Mantener categoría actual")

        for categoria in categorias:
            opciones.append(
                f"{categoria.id} - {categoria.nombre}"
            )

        seleccion = questionary.select(
            "Seleccioná una categoría:",
            choices=opciones
        ).ask()

        if seleccion is None:
            return None
        if seleccion == "Mantener categoría actual":
            return categoria_actual
        for categoria in categorias:
            if seleccion == f"{categoria.id} - {categoria.nombre}":
                return categoria
        return None


# GESTIÓN DE USUARIOS

    def _menu_usuarios(self) -> None:
        self._mostrar_submenu(
            "USUARIOS",
            ["Listar", "Crear", "Editar", "Eliminar", "Volver"]
        )


# GESTIÓN DE PEDIDOS

    def _menu_pedidos(self) -> None:
        self._mostrar_submenu(
            "PEDIDOS",
            ["Listar", "Crear", "Actualizar", "Eliminar", "Volver"]
        )


# SUBMENÚ PROVISIONAL

    def _mostrar_submenu(
        self,
        titulo: str,
        opciones: list[str]
    ) -> None:

        while True:
            limpiar_consola()
            mostrar_titulo(titulo)
            seleccion = mostrar_menu(
                "Seleccioná una operación:",
                opciones
            )

            if seleccion is None or seleccion == "Volver":
                break
            mostrar_aviso(
                f"La operación '{seleccion}' todavía no está implementada."
            )
            pausar()
