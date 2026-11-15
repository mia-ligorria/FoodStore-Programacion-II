# ==================================================
# Clase Base
# Clase padre de todas las entidades del sistema.
# ==================================================

from abc import ABC, abstractmethod
from datetime import datetime

class Base(ABC):
    """
    Clase abstracta que proporciona atributos y métodos
    comunes a todas las entidades del sistema.
    """
    __contador_id: int = 0

    def __init__(self) -> None:
        Base.__contador_id += 1

        self.__id: int = Base.__contador_id
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TypeError("El valor de eliminado debe ser booleano.")
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Base):
            return False

        return self.id == otro.id

    @abstractmethod
    def __str__(self) -> str:
        pass