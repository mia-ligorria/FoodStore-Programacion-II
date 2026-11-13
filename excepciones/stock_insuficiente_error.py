from excepciones.food_store_error import FoodStoreError


class StockInsuficienteError(FoodStoreError):
    """Se produce cuando no hay stock suficiente para una operación."""
    pass