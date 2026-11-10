from entidades.base import Base
from enums.rol import Rol
from enums.estado import Estado
from enums.forma_pago import FormaPago


class EntidadPrueba(Base):
    def __str__(self) -> str:
        return f"Entidad de prueba - ID: {self.id}"


# Crear dos entidades
entidad1 = EntidadPrueba()
entidad2 = EntidadPrueba()

print("=== PRUEBA DE BASE ===")
print("ID entidad 1:", entidad1.id)
print("ID entidad 2:", entidad2.id)

# Probar comparación
print("¿Son iguales?", entidad1 == entidad2)

# Probar baja lógica
entidad1.eliminar()
print("¿Entidad 1 eliminada?", entidad1.eliminado)

# Probar enumerados
print("\n=== PRUEBA DE ENUMERADOS ===")
print("Rol:", Rol.ADMIN)
print("Estado:", Estado.PENDIENTE)
print("Forma de pago:", FormaPago.EFECTIVO)


from entidades.usuario import Usuario

print("\n=== PRUEBA DE USUARIO ===")

usuario = Usuario(
    nombre="Romina",
    apellido="Castro",
    email="romina@gmail.com",
    contrasena="123456",
    rol=Rol.ADMIN
)

print("ID:", usuario.id)
print(usuario)
print("Nombre:", usuario.nombre)
print("Email:", usuario.email)
print("Rol:", usuario.rol)


from entidades.pedido import Pedido
from entidades.detalle_pedido import DetallePedido

print("\n=== PRUEBA DE PEDIDO ===")

pedido = Pedido(usuario, FormaPago.EFECTIVO)

detalle1 = DetallePedido(
    producto="Hamburguesa",
    cantidad=2,
    precio_unitario=5000
)

detalle2 = DetallePedido(
    producto="Gaseosa",
    cantidad=1,
    precio_unitario=2000
)

pedido.agregar_detalle(detalle1)
pedido.agregar_detalle(detalle2)

print(pedido)
print("Estado:", pedido.estado)
print("Forma de pago:", pedido.forma_pago)
print("Cantidad de detalles:", len(pedido.detalles))
print("Total del pedido:", pedido.calcular_total())