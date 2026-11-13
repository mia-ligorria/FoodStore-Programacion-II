# ==================================================
# EXCEPCIONES PERSONALIZADAS - FOOD STORE
# ==================================================

class FoodStoreError(Exception):
    """Excepción base del sistema Food Store."""
    pass

class EntidadNoEncontradaError(FoodStoreError):
    """La entidad solicitada no existe o está eliminada."""
    pass

class DatoInvalidoError(FoodStoreError):
    """El dato ingresado no cumple las validaciones."""
    pass

class PrecioInvalidoError(DatoInvalidoError):
    """El precio no puede ser negativo."""
    pass

class StockInsuficienteError(FoodStoreError):
    """No hay stock suficiente para realizar la operación."""
    pass

class DuplicadoError(FoodStoreError):
    """El elemento que se intenta registrar ya existe."""
    pass

class OperacionNoPermitidaError(FoodStoreError):
    """La operación no está permitida por las reglas del sistema."""
    pass

class CredencialesInvalidasError(FoodStoreError):
    """El mail o la contraseña son incorrectos."""
    pass
