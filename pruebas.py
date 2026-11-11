from entidades.base import Base
from enums.rol import Rol
from enums.estado import Estado
from enums.forma_pago import FormaPago
from entidades.usuario import Usuario
from entidades.pedido import Pedido
from entidades.detalle_pedido import DetallePedido
from servicios.usuario_servicio import UsuarioServicio
from excepciones.duplicado_error import DuplicadoError
from excepciones.dato_invalido_error import DatoInvalidoError
from excepciones.entidad_no_encontrada_error import EntidadNoEncontradaError
from excepciones.credenciales_invalidas_error import CredencialesInvalidasError


class EntidadPrueba(Base):
    def __str__(self) -> str:
        return f"Entidad de prueba - ID: {self.id}"


# Creo dos entidades
entidad1 = EntidadPrueba()
entidad2 = EntidadPrueba()

print("=== PRUEBA DE BASE ===")
print("ID entidad 1:", entidad1.id)
print("ID entidad 2:", entidad2.id)

# Pruebo comparación
print("¿Son iguales?", entidad1 == entidad2)

# Pruebo baja lógica
entidad1.eliminar()
print("¿Entidad 1 eliminada?", entidad1.eliminado)

# Pruebo enumerados
print("\n=== PRUEBA DE ENUMERADOS ===")
print("Rol:", Rol.ADMIN)
print("Estado:", Estado.PENDIENTE)
print("Forma de pago:", FormaPago.EFECTIVO)



print("\n=== PRUEBA DE USUARIO ===")

usuario = Usuario(
    nombre="Romina",
    apellido="Castro",
    mail="romina@gmail.com",
    celular="2994000000",
    contrasenia="123456",
    rol=Rol.ADMIN
)

print("ID:", usuario.id)
print(usuario)
print("Nombre:", usuario.nombre)
print("Mail:", usuario.mail)
print("Celular:", usuario.celular)
print("Rol:", usuario.rol)
print("Contraseña correcta:", usuario.verificar_contrasenia("123456"))
print("Contraseña incorrecta:", usuario.verificar_contrasenia("000000"))



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




print("\n=== PRUEBA DE USUARIO SERVICIO ===")

servicio_usuarios = UsuarioServicio()

# Creo un administrador para realizar las operaciones
admin_sesion = servicio_usuarios.crear_usuario(
    nombre="Romina",
    apellido="Castro",
    mail="romina@gmail.com",
    celular="2994000000",
    contrasenia="123456",
    rol=Rol.ADMIN
)

# Creo usuario
usuario_nuevo = servicio_usuarios.crear_usuario(
    nombre="Ana",
    apellido="Perez",
    mail="ana@gmail.com",
    celular="2994111111",
    contrasenia="abc123",
    rol=Rol.USUARIO
)

print("Usuario creado:", usuario_nuevo)
print("ID generado:", usuario_nuevo.id)

# Listo usuarios
print("\nListado de usuarios:")
for usuario in servicio_usuarios.listar_usuarios():
    print(usuario)

# Busco por ID
usuario_buscado = servicio_usuarios.buscar_por_id(usuario_nuevo.id)
print("\nUsuario encontrado:", usuario_buscado)

# Intento registrar un mail duplicado
try:
    servicio_usuarios.crear_usuario(
        nombre="Otro",
        apellido="Usuario",
        mail="ana@gmail.com",
        celular="2994222222",
        contrasenia="456789",
        rol=Rol.USUARIO
    )
except DuplicadoError as error:
    print("\nError esperado:", error)



print("\n=== PRUEBA DE EDICIÓN DE USUARIO ===")

# Modifico usuario correctamente
usuario_editado = servicio_usuarios.editar_usuario(
    usuario_sesion=admin_sesion,
    id_usuario=usuario_nuevo.id,
    nombre="Ana María",
    apellido="Perez",
    mail="anamaria@gmail.com",
    celular="2994333333"
)

print("Usuario editado:", usuario_editado)

# Intento utilizar un mail duplicado
try:
    servicio_usuarios.editar_usuario(
        usuario_sesion=admin_sesion,
        id_usuario=usuario_nuevo.id,
        nombre="Ana",
        apellido="Perez",
        mail="romina@gmail.com",
        celular="2994333333"
    )
except DuplicadoError as error:
    print("Error esperado:", error)

# Intento modificar un usuario inexistente
try:
    servicio_usuarios.editar_usuario(
        usuario_sesion=admin_sesion,
        id_usuario=999,
        nombre="Usuario",
        apellido="Inexistente",
        mail="inexistente@gmail.com",
        celular="2994000000"
    )
except EntidadNoEncontradaError as error:
    print("Error esperado:", error)


    print("\n=== PRUEBA DE ELIMINACIÓN DE USUARIO ===")

# Elimino usuario
servicio_usuarios.eliminar_usuario(
    usuario_sesion=admin_sesion,
    id_usuario=usuario_nuevo.id
)

print("¿Usuario eliminado?:", usuario_nuevo.eliminado)

# Compruebo que ya no aparece en el listado
print("\nUsuarios activos:")
for usuario in servicio_usuarios.listar_usuarios():
    print(usuario)

# Intento buscar el usuario eliminado
try:
    servicio_usuarios.buscar_por_id(usuario_nuevo.id)
except EntidadNoEncontradaError as error:
    print("Error esperado:", error)



    print("\n=== PRUEBA DE AUTENTICACIÓN ===")

# Creo un usuario nuevo para probar el inicio de sesión
usuario_login = servicio_usuarios.crear_usuario(
    nombre="Carlos",
    apellido="Lopez",
    mail="carlos@gmail.com",
    celular="2994555555",
    contrasenia="clave123",
    rol=Rol.USUARIO
)

# Intento iniciar sesión correctamente
usuario_autenticado = servicio_usuarios.autenticar(
    mail="carlos@gmail.com",
    contrasenia="clave123"
)

print("Inicio de sesión correcto:", usuario_autenticado)

# Intento iniciar sesión con contraseña incorrecta
try:
    servicio_usuarios.autenticar(
        mail="carlos@gmail.com",
        contrasenia="incorrecta"
    )
except CredencialesInvalidasError as error:
    print("Error esperado:", error)

# Intento iniciar sesión con un mail inexistente
try:
    servicio_usuarios.autenticar(
        mail="noexiste@gmail.com",
        contrasenia="clave123"
    )
except CredencialesInvalidasError as error:
    print("Error esperado:", error)

# Intento iniciar sesión con un usuario eliminado
try:
    servicio_usuarios.autenticar(
        mail="anamaria@gmail.com",
        contrasenia="123456"
    )
except CredencialesInvalidasError as error:
    print("Error esperado:", error)


# Intento eliminar al administrador que tiene la sesión iniciada
try:
    servicio_usuarios.eliminar_usuario(
        usuario_sesion=admin_sesion,
        id_usuario=admin_sesion.id
    )
except DatoInvalidoError as error:
    print("\nError esperado:", error)