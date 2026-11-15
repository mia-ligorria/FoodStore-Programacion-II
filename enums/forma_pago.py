# ==================================================
# Clase FormaPago
# Define los medios de pago disponibles en el sistema.
# ==================================================

from enum import Enum


class FormaPago(Enum):
    TARJETA = 1
    TRANSFERENCIA = 2
    EFECTIVO = 3