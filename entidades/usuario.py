
from entidades.base import Base
from enums.rol import Rol


class Usuario(Base):

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol
    ) -> None:
        super().__init__()

        self.__nombre: str = nombre
        self.__apellido: str = apellido
        self.__mail: str = mail
        self.__celular: str = celular
        self.__contrasenia: str = contrasenia
        self.__rol: Rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        self.__apellido = valor

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        self.__mail = valor

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self.__celular = valor

    @property
    def rol(self) -> Rol:
        return self.__rol

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        return (
            f"Usuario: {self.__nombre} {self.__apellido} | "
            f"Mail: {self.__mail} | "
            f"Celular: {self.__celular} | "
            f"Rol: {self.__rol.name}"
        )
