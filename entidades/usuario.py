from entidades.base import Base
from enums.rol import Rol


class Usuario(Base):

    def __init__(
        self,
        nombre: str,
        apellido: str,
        email: str,
        contrasena: str,
        rol: Rol
    ) -> None:
        super().__init__()

        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__contrasena = contrasena
        self.__rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def apellido(self) -> str:
        return self.__apellido

    @property
    def email(self) -> str:
        return self.__email

    @property
    def contrasena(self) -> str:
        return self.__contrasena

    @property
    def rol(self) -> Rol:
        return self.__rol

    def __str__(self) -> str:
        return (
            f"Usuario: {self.__nombre} {self.__apellido} | "
            f"Email: {self.__email} | "
            f"Rol: {self.__rol.name}"
        )