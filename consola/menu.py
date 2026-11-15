# ==================================================
# CLASE BASE MENU
# Clase padre de los menús del sistema Food Store
# ==================================================

from entidades.usuario import Usuario

class Menu:
    def __init__(self, usuario: Usuario) -> None:
        self._usuario: Usuario = usuario

    def mostrar(self) -> bool:
        raise NotImplementedError(
            "Cada menú debe implementar su propio método mostrar()."
        )
