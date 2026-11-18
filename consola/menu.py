# ==================================================
# CLASE BASE MENU
# Clase padre de los menús del sistema Food Store
# ==================================================
from abc import ABC, abstractmethod
from entidades.usuario import Usuario

class Menu(ABC):
    """
    Clase abstracta que define la estructura común
    de los menús del sistema.
    """

    def __init__(self, usuario: Usuario) -> None:
        self._usuario: Usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        # Muestra el menú correspondiente al rol del usuario.
        pass