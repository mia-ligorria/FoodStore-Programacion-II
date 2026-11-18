# ==================================================
# Clase Usuario
# Representa a un usuario del sistema y sus datos de acceso.
# ==================================================

from entidades.base import Base
from enums.rol import Rol
from excepciones import DatoInvalidoError


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

        if not isinstance(rol, Rol):
            raise TypeError("El rol debe ser un valor válido de Rol.")
        if not isinstance(contrasenia, str):
            raise TypeError("La contraseña debe ser un texto.")
        if not contrasenia.strip():
            raise DatoInvalidoError("La contraseña no puede estar vacía.")
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia: str = contrasenia
        self.__rol: Rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser un texto.")
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip().title()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El apellido debe ser un texto.")
        if not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío.")
        self.__apellido = valor.strip().title()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El mail debe ser un texto.")
        valor = valor.strip().lower()
        if not valor:
            raise DatoInvalidoError("El mail no puede estar vacío.")
        if "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El formato del mail no es válido.")
        self.__mail = valor

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El celular debe ser un texto.")
        if not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío.")
        self.__celular = valor.strip()

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
