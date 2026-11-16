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
from servicios.pedido_servicio import PedidoServicio
from enums.estado import Estado
from enums.forma_pago import FormaPago
from entidades.pedido import Pedido
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
from servicios.usuario_servicio import UsuarioServicio


class MenuAdministrador(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        pedido_servicio: PedidoServicio,
        usuario_servicio: UsuarioServicio
    ) -> None:
        super().__init__(usuario)
        self.__categoria_servicio: CategoriaServicio = categoria_servicio
        self.__producto_servicio: ProductoServicio = producto_servicio
        self.__pedido_servicio: PedidoServicio = pedido_servicio
        self.__usuario_servicio: UsuarioServicio = usuario_servicio



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
        while True:
            limpiar_consola()
            mostrar_titulo("GESTIÓN DE USUARIOS")

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
                    self._listar_usuarios()
                case "Crear":
                    self._crear_usuario()
                case "Editar":
                    self._editar_usuario()
                case "Eliminar":
                    self._eliminar_usuario()
                case None | "Volver":
                    break



    def _listar_usuarios(self) -> None:
        limpiar_consola()
        mostrar_titulo("LISTADO DE USUARIOS")

        try:
            usuarios = self.__usuario_servicio.listar_usuarios()

            if not usuarios:
                mostrar_aviso("No hay usuarios registrados.")
            else:
                for usuario in usuarios:
                    print(
                        f"\nID: {usuario.id}"
                        f"\nNombre: {usuario.nombre}"
                        f"\nApellido: {usuario.apellido}"
                        f"\nMail: {usuario.mail}"
                        f"\nRol: {usuario.rol.name}"
                    )
                    print("-" * 50)

        except FoodStoreError as error:
            mostrar_error(str(error))

        pausar()


    # ==============================================
    # CREAR USUARIO
    # ==============================================

    def _crear_usuario(self) -> None:
        limpiar_consola()
        mostrar_titulo("CREAR USUARIO")

        try:
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            mail = input("Correo electrónico: ").strip()
            celular = input("Celular: ").strip()
            contrasenia = input("Contraseña: ").strip()

            print("\nSeleccioná el rol:")
            roles = ["ADMIN", "USUARIO"]

            seleccion_rol = questionary.select(
                "Rol del usuario:",
                choices=roles
            ).ask()

            if seleccion_rol is None:
                mostrar_aviso("Operación cancelada.")
                pausar()
                return

            from enums.rol import Rol

            rol = Rol[seleccion_rol]

            self.__usuario_servicio.crear_usuario(
                nombre=nombre,
                apellido=apellido,
                mail=mail,
                celular=celular,
                contrasenia=contrasenia,
                rol=rol
            )

            mostrar_exito("Usuario creado correctamente.")

        except FoodStoreError as error:
            mostrar_error(str(error))

        except (ValueError, TypeError) as error:
            mostrar_error(str(error))

        pausar()


    # ==============================================
    # EDITAR USUARIO
    # ==============================================

    def _editar_usuario(self) -> None:
        limpiar_consola()
        mostrar_titulo("EDITAR USUARIO")

        try:
            usuarios = self.__usuario_servicio.listar_usuarios()

            if not usuarios:
                mostrar_aviso("No hay usuarios registrados.")
                pausar()
                return

            self._listar_usuarios()

            id_usuario = int(input("\nIngresá el ID del usuario a editar: "))

            usuario = self.__usuario_servicio.buscar_por_id(id_usuario)

            print("\nDejá vacío un campo si querés conservar el dato actual.")

            nombre = input(f"Nombre [{usuario.nombre}]: ").strip()
            apellido = input(f"Apellido [{usuario.apellido}]: ").strip()
            mail = input(f"Mail [{usuario.mail}]: ").strip()
            celular = input(f"Celular [{usuario.celular}]: ").strip()

            self.__usuario_servicio.editar_usuario(
                usuario_sesion=self.__usuario,
                id_usuario=id_usuario,
                nombre=nombre or usuario.nombre,
                apellido=apellido or usuario.apellido,
                mail=mail or usuario.mail,
                celular=celular or usuario.celular
            )

            mostrar_exito("Usuario actualizado correctamente.")

        except ValueError:
            mostrar_error("El ID debe ser un número entero.")

        except FoodStoreError as error:
            mostrar_error(str(error))

        pausar()


        # ==============================================
    # ELIMINAR USUARIO
    # ==============================================

    def _eliminar_usuario(self) -> None:
        limpiar_consola()
        mostrar_titulo("ELIMINAR USUARIO")

        try:
            usuarios = self.__usuario_servicio.listar_usuarios()

            if not usuarios:
                mostrar_aviso("No hay usuarios registrados.")
                pausar()
                return

            self._listar_usuarios()

            id_usuario = int(input("\nIngresá el ID del usuario a eliminar: "))

            usuario = self.__usuario_servicio.buscar_por_id(id_usuario)

            confirmar = questionary.confirm(
                f"¿Estás seguro de eliminar a {usuario.nombre} "
                f"{usuario.apellido}?"
            ).ask()

            if not confirmar:
                mostrar_aviso("Operación cancelada.")
                pausar()
                return

            self.__usuario_servicio.eliminar_usuario(
                usuario_sesion=self.__usuario,
                id_usuario=id_usuario
            )

            mostrar_exito("Usuario eliminado correctamente.")

        except ValueError:
            mostrar_error("El ID debe ser un número entero.")

        except FoodStoreError as error:
            mostrar_error(str(error))

        pausar()


# GESTIÓN DE PEDIDOS


    def _menu_pedidos(self) -> None:
        while True:
            limpiar_consola()
            mostrar_titulo("GESTIÓN DE PEDIDOS")

            opciones: list[str] = [
                "Listar",
                "Crear",
                "Actualizar",
                "Eliminar",
                "Volver"
            ]

            seleccion = mostrar_menu(
                "Seleccioná una operación:",
                opciones
            )

            match seleccion:
                case "Listar":
                    self._listar_pedidos()
                case "Crear":
                    self._crear_pedido()
                case "Actualizar":
                    self._actualizar_pedido()
                case "Eliminar":
                    self._eliminar_pedido()
                case None | "Volver":
                    break


    def _listar_pedidos(self) -> None:
        limpiar_consola()
        mostrar_titulo("LISTADO DE PEDIDOS")

        try:
            pedidos = self.__pedido_servicio.listar_pedidos(
                self._usuario
            )

            if not pedidos:
                mostrar_aviso("No hay pedidos registrados.")
            else:
                for pedido in pedidos:
                    print(
                        f"\nID: {pedido.id}"
                        f"\nCliente: {pedido.usuario.nombre} "
                        f"{pedido.usuario.apellido}"
                        f"\nEstado: {pedido.estado.name}"
                        f"\nForma de pago: {pedido.forma_pago.name}"
                        f"\nFecha: {pedido.fecha}"
                        f"\nTotal: ${pedido.total:.2f}"
                    )
                    print("-" * 50)

        except FoodStoreError as error:
            mostrar_error(str(error))

        pausar()


        # ==============================================
    # ACTUALIZAR PEDIDO
    # ==============================================

    def _actualizar_pedido(self) -> None:
        limpiar_consola()
        mostrar_titulo("ACTUALIZAR PEDIDO")

        try:
            pedidos = self.__pedido_servicio.listar_pedidos(
                self.__usuario
            )

            if not pedidos:
                mostrar_aviso("No hay pedidos registrados.")
                pausar()
                return

            self._listar_pedidos()

            id_pedido = int(
                input("\nIngresá el ID del pedido a actualizar: ")
            )

            pedido = self.__pedido_servicio.buscar_por_id(
                self.__usuario,
                id_pedido
            )

            print(f"\nPedido seleccionado: {pedido.id}")
            print(f"Estado actual: {pedido.estado.name}")
            print(f"Forma de pago actual: {pedido.forma_pago.name}")

            # Seleccionar nuevo estado
            nuevo_estado_nombre = questionary.select(
                "Seleccioná el nuevo estado:",
                choices=[estado.name for estado in Estado]
            ).ask()

            if nuevo_estado_nombre is None:
                mostrar_aviso("Operación cancelada.")
                pausar()
                return

            nuevo_estado = Estado[nuevo_estado_nombre]

            # Seleccionar nueva forma de pago
            nueva_forma_pago_nombre = questionary.select(
                "Seleccioná la nueva forma de pago:",
                choices=[forma.name for forma in FormaPago]
            ).ask()

            if nueva_forma_pago_nombre is None:
                mostrar_aviso("Operación cancelada.")
                pausar()
                return

            nueva_forma_pago = FormaPago[nueva_forma_pago_nombre]

            self.__pedido_servicio.actualizar_pedido(
                usuario_sesion=self.__usuario,
                id_pedido=id_pedido,
                nuevo_estado=nuevo_estado,
                nueva_forma_pago=nueva_forma_pago
            )

            mostrar_exito("Pedido actualizado correctamente.")

        except ValueError:
            mostrar_error("El ID debe ser un número entero.")

        except FoodStoreError as error:
            mostrar_error(str(error))

        pausar()


        # ==============================================
    # ELIMINAR PEDIDO
    # ==============================================

    def _eliminar_pedido(self) -> None:
        limpiar_consola()
        mostrar_titulo("ELIMINAR PEDIDO")

        try:
            pedidos = self.__pedido_servicio.listar_pedidos(
                self.__usuario
            )

            if not pedidos:
                mostrar_aviso("No hay pedidos registrados.")
                pausar()
                return

            self._listar_pedidos()

            id_pedido = int(
                input("\nIngresá el ID del pedido a eliminar: ")
            )

            pedido = self.__pedido_servicio.buscar_por_id(
                self.__usuario,
                id_pedido
            )

            confirmar = questionary.confirm(
                f"¿Estás seguro de eliminar el pedido {pedido.id}?"
            ).ask()

            if not confirmar:
                mostrar_aviso("Operación cancelada.")
                pausar()
                return

            self.__pedido_servicio.eliminar_pedido(
                usuario_sesion=self.__usuario,
                id_pedido=id_pedido
            )

            mostrar_exito("Pedido eliminado correctamente.")

        except ValueError:
            mostrar_error("El ID debe ser un número entero.")

        except FoodStoreError as error:
            mostrar_error(str(error))

        pausar()


    def _crear_pedido(self) -> None:
        limpiar_consola()
        mostrar_titulo("CREAR PEDIDO")

        try:
            # Seleccionar cliente
            usuarios = self.__usuario_servicio.listar_usuarios()

            if not usuarios:
                mostrar_aviso("No hay usuarios registrados.")
                pausar()
                return

            opciones_usuarios = [
                f"{usuario.id} - {usuario.nombre} {usuario.apellido}"
                for usuario in usuarios
                if usuario.rol.name == "USUARIO"
            ]

            if not opciones_usuarios:
                mostrar_aviso("No hay clientes disponibles.")
                pausar()
                return

            cliente_seleccionado = questionary.select(
                "Seleccioná el cliente:",
                choices=opciones_usuarios
            ).ask()

            if cliente_seleccionado is None:
                return

            id_usuario = int(cliente_seleccionado.split(" - ")[0])

            # Seleccionar productos
            productos = self.__producto_servicio.listar_disponibles()

            if not productos:
                mostrar_aviso("No hay productos disponibles con stock.")
                pausar()
                return

            detalles: list[tuple[int, int]] = []

            while True:
                opciones_productos = [
                    f"{producto.id} - {producto.nombre} "
                    f"(${producto.precio:.2f}) - Stock: {producto.stock}"
                    for producto in productos
                ]

                producto_seleccionado = questionary.select(
                    "Seleccioná un producto:",
                    choices=opciones_productos + ["Finalizar selección"]
                ).ask()

                if producto_seleccionado is None:
                    return

                if producto_seleccionado == "Finalizar selección":
                    break

                id_producto = int(producto_seleccionado.split(" - ")[0])

                cantidad_ingresada = questionary.text(
                    "Ingresá la cantidad:"
                ).ask()

                if cantidad_ingresada is None:
                    return

                cantidad = int(cantidad_ingresada)

                detalles.append((id_producto, cantidad))

            if not detalles:
                mostrar_aviso("El pedido debe tener al menos un producto.")
                pausar()
                return

            # Seleccionar forma de pago
            forma_pago_seleccionada = questionary.select(
                "Seleccioná la forma de pago:",
                choices=[
                    f"{indice + 1} - {forma.name}"
                    for indice, forma in enumerate(FormaPago)
                ]
            ).ask()

            if forma_pago_seleccionada is None:
                return

            numero_forma_pago = int(forma_pago_seleccionada.split(" - ")[0])
            forma_pago = list(FormaPago)[numero_forma_pago - 1]

            # Crear pedido mediante el servicio
            pedido = self.__pedido_servicio.crear_pedido(
                usuario_sesion=self._usuario,
                id_usuario=id_usuario,
                forma_pago=forma_pago,
                detalles=detalles
            )

            mostrar_exito(
                f"Pedido creado correctamente. ID: {pedido.id}\n"
                f"Total: ${pedido.total:.2f}"
            )

        except (FoodStoreError, TypeError, ValueError) as error:
            mostrar_error(str(error))

        pausar()
   


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
