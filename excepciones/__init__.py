# ==================================================
# PAQUETE DE EXCEPCIONES - FOOD STORE
# ==================================================
# Este archivo permite importar las excepciones directamente
# desde el paquete "excepciones", sin tener que indicar
# el nombre del archivo excepciones.py en cada importación.
# ==================================================

from .excepciones import (
    FoodStoreError,
    EntidadNoEncontradaError,
    DatoInvalidoError,
    PrecioInvalidoError,
    StockInsuficienteError,
    DuplicadoError,
    OperacionNoPermitidaError,
    CredencialesInvalidasError
)