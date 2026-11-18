# ==================================================
# Clase UsuarioServicio
# Gestiona el registro, búsqueda, edición, eliminación
# y autenticación de los usuarios del sistema.
# ==================================================

from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones import (
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    CredencialesInvalidasError,
    OperacionNoPermitidaError
)

class UsuarioServicio:
    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []


    def __validar_administrador(
        self,
        usuario_sesion: Usuario
    ) -> None:

        if not isinstance(usuario_sesion, Usuario):
            raise DatoInvalidoError("El usuario de sesión no es válido.")
        if usuario_sesion.eliminado:
            raise OperacionNoPermitidaError("Un usuario eliminado no puede realizar operaciones.")
        if usuario_sesion.rol != Rol.ADMIN:
            raise OperacionNoPermitidaError("No tenés permisos para realizar esta operación.")

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol
    ) -> Usuario:

        if not isinstance(nombre, str) or not isinstance(apellido, str):
            raise TypeError("El nombre y el apellido deben ser textos.")

        if not isinstance(mail, str):
            raise TypeError("El mail debe ser un texto.")

        if not isinstance(celular, str):
            raise TypeError("El celular debe ser un texto.")

        if not isinstance(contrasenia, str):
            raise TypeError("La contraseña debe ser un texto.")
        
        mail = mail.strip().lower()

        if not nombre.strip() or not apellido.strip():
            raise DatoInvalidoError("El nombre y el apellido son obligatorios.")

        if not mail.strip() or "@" not in mail or "." not in mail:
            raise DatoInvalidoError("El mail no tiene un formato válido.")

        if any(
            usuario.mail == mail
            for usuario in self.__usuarios
            if not usuario.eliminado
        ):
            raise DuplicadoError("Ya existe un usuario con ese mail.")

        if not celular.strip():
            raise DatoInvalidoError("El celular es obligatorio.")

        if not contrasenia.strip():
            raise DatoInvalidoError("La contraseña es obligatoria.")

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            mail=mail,
            celular=celular,
            contrasenia=contrasenia,
            rol=rol
        )

        self.__usuarios.append(usuario)
        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        return [
            usuario for usuario in self.__usuarios
            if not usuario.eliminado
        ]

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario

        raise EntidadNoEncontradaError(
            f"No se encontró un usuario activo con ID {id_usuario}."
        )


    def editar_usuario(
        self,
        usuario_sesion: Usuario,
        id_usuario: int,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str
    ) -> Usuario:

        self.__validar_administrador(usuario_sesion)
        
        if not isinstance(nombre, str) or not isinstance(apellido, str):
            raise TypeError("El nombre y el apellido deben ser textos.")
        if not isinstance(mail, str):
            raise TypeError("El mail debe ser un texto.")
        if not isinstance(celular, str):
            raise TypeError("El celular debe ser un texto.")
        
        usuario = self.buscar_por_id(id_usuario)

        if not nombre.strip() or not apellido.strip():
            raise DatoInvalidoError(
                "El nombre y el apellido son obligatorios."
            )

        if not mail.strip() or "@" not in mail or "." not in mail:
            raise DatoInvalidoError("El mail no tiene un formato válido.")
        mail = mail.strip().lower()

        for otro_usuario in self.__usuarios:
            if(
                otro_usuario.id != id_usuario
                and not otro_usuario.eliminado
                and otro_usuario.mail == mail
            ):
                raise DuplicadoError(
                    "Ya existe otro usuario con ese mail."
                )

        if not celular.strip():
            raise DatoInvalidoError("El celular es obligatorio.")

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.mail = mail
        usuario.celular = celular

        return usuario


    def eliminar_usuario(
        self,
        usuario_sesion: Usuario,
        id_usuario: int
    ) -> None:

        if usuario_sesion.rol != Rol.ADMIN:
            raise OperacionNoPermitidaError(
                "No tenés permisos para eliminar usuarios."
            )

        if usuario_sesion.eliminado:
            raise OperacionNoPermitidaError(
                "Un usuario eliminado no puede realizar operaciones."
            )

        if usuario_sesion.id == id_usuario:
            raise OperacionNoPermitidaError(
                "No podés eliminar tu propio usuario mientras tenés la sesión iniciada."
            )

        usuario = self.buscar_por_id(id_usuario)
        usuario.eliminado = True


    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        if not isinstance(mail, str) or not isinstance(contrasenia, str):
            raise CredencialesInvalidasError(
                "Mail o contraseña incorrectos."
            )
        mail = mail.strip().lower()

        for usuario in self.__usuarios:
            if (
                usuario.mail == mail
                and not usuario.eliminado
                and usuario.verificar_contrasenia(contrasenia)
            ):
                return usuario
        raise CredencialesInvalidasError(
            "Mail o contraseña incorrectos."
        )