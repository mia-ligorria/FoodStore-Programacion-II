# ==================================================
# Clase Rol
# Define los roles de los usuarios del sistema.
# ==================================================

from enum import Enum


class Rol(Enum):
    ADMIN = 1
    USUARIO = 2