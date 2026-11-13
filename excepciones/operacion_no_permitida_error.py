from excepciones.food_store_error import FoodStoreError


class OperacionNoPermitidaError(FoodStoreError):
    """Se produce cuando se intenta realizar una operación no permitida."""
    pass