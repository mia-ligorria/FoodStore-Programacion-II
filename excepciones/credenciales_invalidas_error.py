from excepciones.food_store_error import FoodStoreError


class CredencialesInvalidasError(FoodStoreError):
    """Se utiliza cuando los datos de inicio de sesión son incorrectos."""
    pass