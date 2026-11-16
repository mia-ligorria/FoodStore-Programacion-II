
# ==================================================
# Clase PedidoServicio
# Gestiona la creación, búsqueda y consulta de pedidos.
# ==================================================

from entidades.pedido import Pedido
from entidades.usuario import Usuario
from entidades.producto import Producto
from enums.rol import Rol
from enums.forma_pago import FormaPago
from servicios.usuario_servicio import UsuarioServicio
from servicios.producto_servicio import ProductoServicio
from excepciones import (
    DatoInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError
)
from enums.estado import Estado

class PedidoServicio:

    def __init__(
        self,
        usuario_servicio: UsuarioServicio,
        producto_servicio: ProductoServicio
    ) -> None:
        self.__pedidos: list[Pedido] = []
        self.__usuario_servicio: UsuarioServicio = usuario_servicio
        self.__producto_servicio: ProductoServicio = producto_servicio

    # ==================================================
    # VALIDACIÓN DE PERMISOS
    # ==================================================

    def __validar_administrador(
        self,
        usuario_sesion: Usuario
    ) -> None:

        if not isinstance(usuario_sesion, Usuario):
            raise DatoInvalidoError(
                "El usuario de sesión no es válido."
            )

        if usuario_sesion.eliminado:
            raise OperacionNoPermitidaError(
                "Un usuario eliminado no puede realizar operaciones."
            )

        if usuario_sesion.rol != Rol.ADMIN:
            raise OperacionNoPermitidaError(
                "No tenés permisos para realizar esta operación."
            )

    # ==================================================
    # CREAR PEDIDO
    # ==================================================

    def crear_pedido(
        self,
        usuario_sesion: Usuario,
        id_usuario: int,
        forma_pago: FormaPago,
        detalles: list[tuple[int, int]]
    ) -> Pedido:

        self.__validar_administrador(usuario_sesion)

        if not detalles:
            raise DatoInvalidoError(
                "El pedido debe contener al menos un producto."
            )

        usuario = self.__usuario_servicio.buscar_por_id(id_usuario)

        pedido = Pedido(
            usuario=usuario,
            forma_pago=forma_pago
        )

        # Guardamos el stock original para poder restaurarlo
        # si ocurre un error durante la creación del pedido.
        stocks_originales: dict[int, tuple[Producto, int]] = {}

        try:
            for id_producto, cantidad in detalles:

                producto = self.__producto_servicio.buscar_por_id(
                    id_producto
                )

                if producto is None or producto.eliminado:
                    raise EntidadNoEncontradaError(
                        f"No se encontró un producto activo "
                        f"con ID {id_producto}."
                    )

                # Guardamos el stock original una sola vez
                # por producto.
                if producto.id not in stocks_originales:
                    stocks_originales[producto.id] = (
                        producto,
                        producto.stock
                    )

                # Utilizamos obligatoriamente el método
                # de la entidad Pedido.
                pedido.agregar_detalle(
                    cantidad=cantidad,
                    producto=producto
                )

            # Calculamos el total mediante Calculable.
            pedido.calcular_total()

            # El pedido se incorpora solamente si todo salió bien.
            self.__pedidos.append(pedido)

            return pedido

        except Exception:
            # Si falla algún detalle, restauramos todos
            # los stocks a sus valores originales.
            for producto, stock_original in stocks_originales.values():
                producto.stock = stock_original

            raise

    # ==================================================
    # LISTAR PEDIDOS (ADMINISTRADOR)
    # ==================================================

    def listar_pedidos(
        self,
        usuario_sesion: Usuario
    ) -> list[Pedido]:

        self.__validar_administrador(usuario_sesion)

        return [
            pedido
            for pedido in self.__pedidos
            if not pedido.eliminado
        ]

    # ==================================================
    # BUSCAR PEDIDO POR ID (ADMINISTRADOR)
    # ==================================================

    def buscar_por_id(
        self,
        usuario_sesion: Usuario,
        id_pedido: int
    ) -> Pedido:

        self.__validar_administrador(usuario_sesion)

        for pedido in self.__pedidos:
            if pedido.id == id_pedido and not pedido.eliminado:
                return pedido

        raise EntidadNoEncontradaError(
            f"No se encontró un pedido activo con ID {id_pedido}."
        )

    # ==================================================
    # ACTUALIZAR PEDIDO (ADMINISTRADOR)
    # ==================================================

    def actualizar_pedido(
        self,
        usuario_sesion: Usuario,
        id_pedido: int,
        nuevo_estado: Estado | None = None,
        nueva_forma_pago: FormaPago | None = None
    ) -> Pedido:

        self.__validar_administrador(usuario_sesion)

        if nuevo_estado is None and nueva_forma_pago is None:
            raise DatoInvalidoError(
                "Debe indicar qué dato del pedido desea modificar."
            )

        if nueva_forma_pago is not None and not isinstance(
            nueva_forma_pago, FormaPago
        ):
            raise DatoInvalidoError("La forma de pago no es válida.")

        pedido = self.buscar_por_id(usuario_sesion, id_pedido)

        if nuevo_estado is not None:
            pedido.cambiar_estado(nuevo_estado)

        if nueva_forma_pago is not None:
            pedido.forma_pago = nueva_forma_pago

        return pedido


    # ==================================================
    # ELIMINAR PEDIDO (ADMINISTRADOR)
    # ==================================================

    def eliminar_pedido(
        self,
        usuario_sesion: Usuario,
        id_pedido: int
    ) -> None:

        self.__validar_administrador(usuario_sesion)

        pedido = self.buscar_por_id(usuario_sesion, id_pedido)

        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            for detalle in pedido.detalles:
                producto = detalle.producto
                producto.stock += detalle.cantidad

        for detalle in pedido.detalles:
            detalle.eliminado = True

        pedido.eliminado = True
        

    # ==================================================
    # LISTAR MIS PEDIDOS (CLIENTE)
    # ==================================================

    def listar_mis_pedidos(
        self,
        usuario_sesion: Usuario
    ) -> list[Pedido]:

        if not isinstance(usuario_sesion, Usuario):
            raise DatoInvalidoError(
                "El usuario de sesión no es válido."
            )

        if usuario_sesion.eliminado:
            raise OperacionNoPermitidaError(
                "El usuario está eliminado."
            )

        return [
            pedido
            for pedido in self.__pedidos
            if (
                pedido.usuario.id == usuario_sesion.id
                and not pedido.eliminado
            )
        ]

    # ==================================================
    # BUSCAR MI PEDIDO (CLIENTE)
    # ==================================================

    def buscar_mi_pedido(
        self,
        usuario_sesion: Usuario,
        id_pedido: int
    ) -> Pedido:

        pedidos_usuario = self.listar_mis_pedidos(usuario_sesion)

        for pedido in pedidos_usuario:
            if pedido.id == id_pedido:
                return pedido

        raise EntidadNoEncontradaError(
            f"No se encontró un pedido con ID {id_pedido}."
        )
