# ==================================================
# FOOD STORE - PROGRAMA PRINCIPAL
# Programación II - UTN FRM
# ==================================================

import questionary

from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio

from enums.rol import Rol

from excepciones import FoodStoreError

from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente

from consola.utilidades_consola import (
    limpiar_consola,
    mostrar_titulo,
    mostrar_error,
    mostrar_aviso,
    mostrar_exito,
    pausar
)


def iniciar_sistema() -> None:
    """Inicializa los servicios y ejecuta el sistema."""

    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio(categoria_servicio)
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio(
        usuario_servicio,
        producto_servicio
    )

    # Registro del administrador inicial
    usuario_servicio.crear_usuario(
        nombre="Administrador",
        apellido="FoodStore",
        mail="admin@foodstore.com",
        celular="0000000000",
        contrasenia="admin123",
        rol=Rol.ADMIN
    )

    mostrar_exito("Sistema inicializado correctamente.")

    while True:
        limpiar_consola()
        mostrar_titulo("BIENVENIDO A FOOD STORE")

        # Inicio de sesión
        intentos = 0
        usuario = None

        while intentos < 3:
            mail = questionary.text(
                "Ingresá tu mail:"
            ).ask()

            if mail is None:
                return

            contrasenia = questionary.password(
                "Ingresá tu contraseña:"
            ).ask()

            if contrasenia is None:
                return

            try:
                usuario = usuario_servicio.autenticar(
                    mail,
                    contrasenia
                )

                mostrar_exito(
                    f"Bienvenido/a {usuario.nombre} {usuario.apellido}."
                )
                pausar()
                break

            except FoodStoreError as error:
                intentos += 1
                mostrar_error(str(error))

                if intentos < 3:
                    mostrar_aviso(
                        f"Te quedan {3 - intentos} intentos."
                    )
                    pausar()

        if usuario is None:
            mostrar_error("Se agotaron los tres intentos de acceso.")
            return

        if usuario.rol == Rol.ADMIN:
            menu = MenuAdministrador(
                usuario,
                categoria_servicio,
                producto_servicio,
                pedido_servicio,
                usuario_servicio
            )

        else:
            menu = MenuCliente(
                usuario,
                categoria_servicio,
                producto_servicio,
                pedido_servicio
            )

        continuar = menu.mostrar()

        if not continuar:
            limpiar_consola()
            mostrar_titulo("FOOD STORE")
            mostrar_aviso("Gracias por utilizar nuestro sistema.")
            return

if __name__ == "__main__":
    iniciar_sistema()
