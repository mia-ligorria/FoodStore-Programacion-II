# ==================================================
# MENU CLIENTE - FOOD STORE
# Programación II - UTN FRM
# ==================================================

from entidades.usuario import Usuario
from consola.menu import Menu

from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.pedido_servicio import PedidoServicio

from excepciones import FoodStoreError

from consola.utilidades_consola import (
    limpiar_consola,
    mostrar_titulo,
    mostrar_menu,
    mostrar_aviso,
    mostrar_error,
    pausar
)


class MenuCliente(Menu):

    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        pedido_servicio: PedidoServicio
    ) -> None:

        super().__init__(usuario)

        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio
        self.__pedido_servicio = pedido_servicio

# ==============================================
# MENU PRINCIPAL
# ==============================================

    def mostrar(self) -> bool:
        while True:
            limpiar_consola()

            mostrar_titulo(
                f"FOOD STORE - CLIENTE "
                f"({self._usuario.nombre} {self._usuario.apellido})"
            )

            opciones = [
                "Ver categorías",
                "Ver productos disponibles",
                "Mis pedidos",
                "Mis datos",
                "Cerrar sesión",                
                "Salir"
            ]

            seleccion = mostrar_menu(
                "Seleccioná una opción:",
                opciones
            )

            match seleccion:
                case "Ver categorías":
                    self._ver_categorias()
                case "Ver productos disponibles":
                    self._ver_productos()
                case "Mis pedidos":
                    self._ver_mis_pedidos()
                case "Mis datos":
                    self._ver_mis_datos()
                case "Cerrar sesión":
                    return True
                case "Salir":
                    return False
                case None:
                    return True

# ==============================================
# CONSULTAR CATEGORÍAS
# ==============================================

    def _ver_categorias(self) -> None:
        limpiar_consola()
        mostrar_titulo("CATEGORÍAS DISPONIBLES")

        categorias = self.__categoria_servicio.listar()

        if not categorias:
            mostrar_aviso("No hay categorías registradas.")
        else:
            for categoria in categorias:
                print(
                    f"\nID: {categoria.id}"
                    f"\nNombre: {categoria.nombre}"
                    f"\nDescripción: {categoria.descripcion}"
                )
                print("-" * 50)

        pausar()

# ==============================================
# CONSULTAR PRODUCTOS
# ==============================================

    def _ver_productos(self) -> None:
        limpiar_consola()
        mostrar_titulo("PRODUCTOS DISPONIBLES")

        productos = self.__producto_servicio.listar_disponibles()

        if not productos:
            mostrar_aviso("No hay productos disponibles.")
        else:
            for producto in productos:
                print(
                    f"\nID: {producto.id}"
                    f"\nNombre: {producto.nombre}"
                    f"\nDescripción: {producto.descripcion}"
                    f"\nPrecio: ${producto.precio:.2f}"
                    f"\nStock: {producto.stock}"
                    f"\nCategoría: {producto.categoria.nombre}"
                )
                print("-" * 50)
        pausar()

# ==============================================
# CONSULTAR MIS PEDIDOS
# ==============================================

    def _ver_mis_pedidos(self) -> None:
        limpiar_consola()
        mostrar_titulo("MIS PEDIDOS")

        try:
            pedidos = self.__pedido_servicio.listar_mis_pedidos(
                self._usuario
            )

            if not pedidos:
                mostrar_aviso("Todavía no tenés pedidos registrados.")
            else:
                print("\nTus pedidos registrados:\n")
                for pedido in pedidos:
                    print(
                        f"ID: {pedido.id}"
                        f"| Fecha: {pedido.fecha}"
                        f"| Estado: {pedido.estado.name}"
                        f"| Total: ${pedido.total:.2f}"
                    )
                print("-" * 50)
                id_pedido = int(
                    input("\nIngresá el ID del pedido que querés consultar: ")
                )

                pedido = self.__pedido_servicio.buscar_mi_pedido(
                    self._usuario,
                    id_pedido
                )

                print("\nDETALLE DEL PEDIDO")
                print(f"ID: {pedido.id}")
                print(f"Fecha: {pedido.fecha}")
                print(f"Estado: {pedido.estado.name}")
                print(f"Forma de pago: {pedido.forma_pago.name}")
                print(f"Total: ${pedido.total:.2f}")
                print("\nProductos:")

                for detalle in pedido.detalles:
                    print(
                        f"- {detalle.producto.nombre}"
                        f"| Cantidad: {detalle.cantidad}"
                        f"| Subtotal: ${detalle.subtotal:.2f}"
                    )
                print("-" * 50)

        except ValueError:
            mostrar_error("El ID debe ser un número entero.")
        except FoodStoreError as error:
            mostrar_error(str(error))
        pausar()



# ==============================================
# CONSULTAR MIS DATOS
# ==============================================

    def _ver_mis_datos(self) -> None:
        limpiar_consola()
        mostrar_titulo("MIS DATOS")

        print(f"\nNombre: {self._usuario.nombre}")
        print(f"Apellido: {self._usuario.apellido}")
        print(f"Mail: {self._usuario.mail}")
        print(f"Celular: {self._usuario.celular}")
        print(f"Rol: {self._usuario.rol.name}")

        print("-" * 50)
        pausar()
