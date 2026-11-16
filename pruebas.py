# ==================================================
# PRUEBAS DE INTEGRACIÓN - FOOD STORE
# Programación II - UTN FRM
# ==================================================

from entidades.base import Base
from entidades.categoria import Categoria
from entidades.producto import Producto
from entidades.usuario import Usuario
from entidades.pedido import Pedido

from enums.rol import Rol
from enums.estado import Estado
from enums.forma_pago import FormaPago

from servicios.usuario_servicio import UsuarioServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio

from excepciones import (
    DuplicadoError, 
    DatoInvalidoError,
    EntidadNoEncontradaError,
    CredencialesInvalidasError,
    OperacionNoPermitidaError
)

from servicios.pedido_servicio import PedidoServicio

# ENTIDAD AUXILIAR PARA PROBAR BASE

class EntidadPrueba(Base):

    def __str__(self) -> str:
        return f"Entidad de prueba - ID: {self.id}"


# PRUEBA DE BASE

print("\n=== PRUEBA DE BASE ===")

entidad1 = EntidadPrueba()
entidad2 = EntidadPrueba()

print("ID entidad 1:", entidad1.id)
print("ID entidad 2:", entidad2.id)

print("¿Son iguales?", entidad1 == entidad2)

# Prueba de baja lógica mediante la propiedad.

entidad1.eliminado = True

print("¿Entidad 1 eliminada?:", entidad1.eliminado)


# PRUEBA DE ENUMERADOS

print("\n=== PRUEBA DE ENUMERADOS ===")

print("Rol:", Rol.ADMIN)
print("Estado:", Estado.PENDIENTE)
print("Forma de pago:", FormaPago.EFECTIVO)


# PRUEBA DE USUARIO

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

print(
    "Contraseña correcta:",
    usuario.verificar_contrasenia("123456")
)

print(
    "Contraseña incorrecta:",
    usuario.verificar_contrasenia("000000")
)


# PRUEBA DE CATEGORÍA Y PRODUCTO

print("\n=== PRUEBA DE CATEGORÍA Y PRODUCTO ===")

categoria = Categoria(
    nombre="Comidas",
    descripcion="Productos alimenticios"
)

producto = Producto(
    nombre="Hamburguesa",
    precio=5000,
    descripcion="Hamburguesa clásica",
    stock=10,
    imagen="hamburguesa.png",
    disponible=True,
    categoria=categoria
)

# Creo los servicios y registro las entidades.

categoria_servicio = CategoriaServicio()
producto_servicio = ProductoServicio(categoria_servicio)

categoria_servicio.agregar(categoria)
producto_servicio.agregar(producto)

print("Categoría:", categoria)
print("Producto:", producto)

print("Productos de la categoría:")

for producto_categoria in categoria.productos:
    print(producto_categoria)

print("Cantidad de productos:", len(categoria.productos))

# Compruebo que el producto también esté registrado en el servicio.

print("Productos registrados en el servicio:", len(producto_servicio.listar()))


# PRUEBAS DE CATEGORIA SERVICIO

print("\n=== PRUEBAS DE CATEGORIA SERVICIO ===")

# PRUEBA DE CATEGORÍA DUPLICADA
try:
    categoria_duplicada = Categoria(
        nombre=" comidas ",
        descripcion="Otra categoría"
    )
    categoria_servicio.agregar(categoria_duplicada)
except DuplicadoError as error:
    print("Error esperado:", error)


# PRUEBA DE ELIMINACIÓN DE CATEGORÍA CON PRODUCTOS ACTIVOS
try:
    categoria_servicio.eliminar(
        categoria.id,
        producto_servicio
    )
except OperacionNoPermitidaError as error:
    print("Error esperado:", error)



# PRUEBAS DE PRODUCTO SERVICIO

print("\n=== PRUEBAS DE PRODUCTO SERVICIO ===")

# CREO DOS CATEGORÍAS NUEVAS
categoria_bebidas = Categoria(
    nombre="Bebidas",
    descripcion="Bebidas y aguas"
)

categoria_almacen = Categoria(
    nombre="Almacén",
    descripcion="Productos de almacén"
)

categoria_servicio.agregar(categoria_bebidas)
categoria_servicio.agregar(categoria_almacen)


# CREO Y REGISTRO UN PRODUCTO
agua = Producto(
    nombre="Agua",
    precio=1000,
    descripcion="Agua mineral",
    stock=10,
    imagen="agua.png",
    disponible=True,
    categoria=categoria_bebidas
)

producto_servicio.agregar(agua)

print("Producto creado:", agua.nombre)
print("Productos en Bebidas:", len(categoria_bebidas.productos))

# PRUEBA DE CAMBIO DE CATEGORÍA
producto_servicio.editar(
    agua.id,
    "Agua mineral",
    1500,
    "Agua mineral sin gas",
    12,
    "agua.png",
    True,
    categoria_almacen
)

print("\nDespués de cambiar la categoría:")
print("Nueva categoría:", agua.categoria.nombre)
print("Productos en Bebidas:", len(categoria_bebidas.productos))
print("Productos en Almacén:", len(categoria_almacen.productos))

# PRUEBA DE ELIMINACIÓN LÓGICA DEL PRODUCTO
producto_servicio.eliminar(agua.id)

print("\nDespués de eliminar el producto:")
print("¿Agua eliminada?:", agua.eliminado)
print("Productos activos en el servicio:", len(producto_servicio.listar()))

# PRUEBA DE ELIMINACIÓN DE CATEGORÍA SIN PRODUCTOS ACTIVOS
categoria_servicio.eliminar(
    categoria_bebidas.id,
    producto_servicio
)

print("\n¿Categoría Bebidas eliminada?:", categoria_bebidas.eliminado)


# PRUEBA DE PEDIDO Y DETALLE PEDIDO

print("\n=== PRUEBA DE PEDIDO Y DETALLE PEDIDO ===")

pedido = Pedido(usuario, FormaPago.EFECTIVO)

print("Pedido creado:", pedido)
print("Estado inicial:", pedido.estado)
print("Forma de pago:", pedido.forma_pago)
print("Cantidad inicial de detalles:", len(pedido.detalles))
print("Total inicial:", pedido.total)

# Agrego un producto al pedido.

pedido.agregar_detalle(2, producto)

print("\nDespués de agregar 2 hamburguesas:")

print("Cantidad de detalles:", len(pedido.detalles))
print("Cantidad del detalle:", pedido.detalles[0].cantidad)
print("Subtotal:", pedido.detalles[0].subtotal)
print("Total:", pedido.total)
print("Stock restante:", producto.stock)

# Agrego el mismo producto nuevamente.
# El pedido debe incrementar la cantidad del detalle existente.

pedido.agregar_detalle(3, producto)

print("\nDespués de agregar otras 3 hamburguesas:")

print("Cantidad de detalles:", len(pedido.detalles))
print("Cantidad acumulada:", pedido.detalles[0].cantidad)
print("Subtotal actualizado:", pedido.detalles[0].subtotal)
print("Total actualizado:", pedido.total)
print("Stock restante:", producto.stock)

# Prueba de cantidad inválida.

try:
    pedido.agregar_detalle(0, producto)

except (DatoInvalidoError, TypeError, ValueError) as error:
    print("\nError esperado:", error)


# PRUEBA DE USUARIO SERVICIO

print("\n=== PRUEBA DE USUARIO SERVICIO ===")

servicio_usuarios = UsuarioServicio()

# Creo un administrador para realizar las operaciones.

admin_sesion = servicio_usuarios.crear_usuario(
    nombre="Romina",
    apellido="Castro",
    mail="romina@gmail.com",
    celular="2994000000",
    contrasenia="123456",
    rol=Rol.ADMIN
)

# Creo un usuario común.

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


# LISTAR USUARIOS

print("\n=== LISTADO DE USUARIOS ===")

for usuario_listado in servicio_usuarios.listar_usuarios():
    print(usuario_listado)


# BUSCAR USUARIO

print("\n=== BÚSQUEDA DE USUARIO ===")

usuario_buscado = servicio_usuarios.buscar_por_id(
    usuario_nuevo.id
)

print("Usuario encontrado:", usuario_buscado)


# PRUEBA DE MAIL DUPLICADO

print("\n=== PRUEBA DE MAIL DUPLICADO ===")

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
    print("Error esperado:", error)


# PRUEBA DE EDICIÓN DE USUARIO

print("\n=== PRUEBA DE EDICIÓN DE USUARIO ===")

usuario_editado = servicio_usuarios.editar_usuario(
    usuario_sesion=admin_sesion,
    id_usuario=usuario_nuevo.id,
    nombre="Ana María",
    apellido="Perez",
    mail="anamaria@gmail.com",
    celular="2994333333"
)

print("Usuario editado:", usuario_editado)


# Intento utilizar un mail duplicado.

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


# Intento modificar un usuario inexistente.

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


# PRUEBA DE ELIMINACIÓN DE USUARIO

print("\n=== PRUEBA DE ELIMINACIÓN DE USUARIO ===")

servicio_usuarios.eliminar_usuario(
    usuario_sesion=admin_sesion,
    id_usuario=usuario_nuevo.id
)

print("¿Usuario eliminado?:", usuario_nuevo.eliminado)

print("\nUsuarios activos:")

for usuario_listado in servicio_usuarios.listar_usuarios():
    print(usuario_listado)


# Intento buscar el usuario eliminado.

try:
    servicio_usuarios.buscar_por_id(usuario_nuevo.id)

except EntidadNoEncontradaError as error:
    print("Error esperado:", error)


# PRUEBA DE AUTENTICACIÓN

print("\n=== PRUEBA DE AUTENTICACIÓN ===")

usuario_login = servicio_usuarios.crear_usuario(
    nombre="Carlos",
    apellido="Lopez",
    mail="carlos@gmail.com",
    celular="2994555555",
    contrasenia="clave123",
    rol=Rol.USUARIO
)

# Inicio de sesión correcto.

usuario_autenticado = servicio_usuarios.autenticar(
    mail="carlos@gmail.com",
    contrasenia="clave123"
)

print("Inicio de sesión correcto:", usuario_autenticado)


# Contraseña incorrecta.

try:
    servicio_usuarios.autenticar(
        mail="carlos@gmail.com",
        contrasenia="incorrecta"
    )

except CredencialesInvalidasError as error:
    print("Error esperado:", error)


# Mail inexistente.

try:
    servicio_usuarios.autenticar(
        mail="noexiste@gmail.com",
        contrasenia="clave123"
    )

except CredencialesInvalidasError as error:
    print("Error esperado:", error)


# Usuario eliminado.

try:
    servicio_usuarios.autenticar(
        mail="anamaria@gmail.com",
        contrasenia="abc123"
    )

except CredencialesInvalidasError as error:
    print("Error esperado:", error)



# ==================================================
# PRUEBAS DE PEDIDO SERVICIO
# ==================================================

print("\n=== PRUEBAS DE PEDIDO SERVICIO ===")

servicio_pedidos = PedidoServicio(
    usuario_servicio=servicio_usuarios,
    producto_servicio=producto_servicio
)

# CREAR PEDIDO DESDE EL SERVICIO

pedido_servicio = servicio_pedidos.crear_pedido(
    usuario_sesion=admin_sesion,
    id_usuario=usuario_login.id,
    forma_pago=FormaPago.EFECTIVO,
    detalles=[(producto.id, 2)]
)

print("Pedido creado:", pedido_servicio)
print("Total:", pedido_servicio.total)
print("Stock después de crear:", producto.stock)

# LISTAR PEDIDOS DEL ADMINISTRADOR

print("\nPedidos registrados:")

for pedido_listado in servicio_pedidos.listar_pedidos(admin_sesion):
    print(pedido_listado)

# CONSULTAR PEDIDOS DEL CLIENTE

print("\nPedidos del cliente:")

for pedido_cliente in servicio_pedidos.listar_mis_pedidos(usuario_login):
    print(pedido_cliente)

# ACTUALIZAR FORMA DE PAGO Y ESTADO

pedido_actualizado = servicio_pedidos.actualizar_pedido(
    usuario_sesion=admin_sesion,
    id_pedido=pedido_servicio.id,
    nuevo_estado=Estado.CONFIRMADO,
    nueva_forma_pago=FormaPago.TRANSFERENCIA
)

print("\nPedido actualizado:")
print("Estado:", pedido_actualizado.estado)
print("Forma de pago:", pedido_actualizado.forma_pago)

# CANCELAR PEDIDO Y COMPROBAR DEVOLUCIÓN DE STOCK

pedido_actualizado = servicio_pedidos.actualizar_pedido(
    usuario_sesion=admin_sesion,
    id_pedido=pedido_servicio.id,
    nuevo_estado=Estado.CANCELADO
)

print("\nPedido cancelado:", pedido_actualizado.estado)
print("Stock después de cancelar:", producto.stock)

# ELIMINAR PEDIDO YA CANCELADO
# El stock no debe devolverse una segunda vez.

servicio_pedidos.eliminar_pedido(
    usuario_sesion=admin_sesion,
    id_pedido=pedido_servicio.id
)

print("¿Pedido eliminado?:", pedido_servicio.eliminado)
print("Stock después de eliminar el cancelado:", producto.stock)

# CREAR OTRO PEDIDO PENDIENTE PARA PROBAR LA ELIMINACIÓN

pedido_pendiente = servicio_pedidos.crear_pedido(
    usuario_sesion=admin_sesion,
    id_usuario=usuario_login.id,
    forma_pago=FormaPago.EFECTIVO,
    detalles=[(producto.id, 1)]
)

print("\nSegundo pedido creado:", pedido_pendiente)
print("Stock antes de eliminar:", producto.stock)

servicio_pedidos.eliminar_pedido(
    usuario_sesion=admin_sesion,
    id_pedido=pedido_pendiente.id
)

print("¿Segundo pedido eliminado?:", pedido_pendiente.eliminado)
print("Stock después de eliminar:", producto.stock)

# CONSULTAR PEDIDO ELIMINADO: DEBE DAR ERROR

try:
    servicio_pedidos.buscar_por_id(
        admin_sesion,
        pedido_pendiente.id
    )
except EntidadNoEncontradaError as error:
    print("Error esperado:", error)


# PRUEBA DE ELIMINACIÓN DEL ADMINISTRADOR EN SESIÓN

print("\n=== PRUEBA DE ELIMINACIÓN DEL ADMINISTRADOR ===")

try:
    servicio_usuarios.eliminar_usuario(
        usuario_sesion=admin_sesion,
        id_usuario=admin_sesion.id
    )
except OperacionNoPermitidaError as e:
    print("Error esperado:", e)

# FIN DE LAS PRUEBAS

print("\n=== FIN DE LAS PRUEBAS ===")