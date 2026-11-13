from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.dato_invalido_error import DatoInvalidoError
from excepciones.duplicado_error import DuplicadoError
from excepciones.entidad_no_encontrada_error import EntidadNoEncontradaError
from excepciones.credenciales_invalidas_error import CredencialesInvalidasError
from excepciones.operacion_no_permitida_error import OperacionNoPermitidaError


class UsuarioServicio:

    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol
    ) -> Usuario:

        if not nombre.strip() or not apellido.strip():
            raise DatoInvalidoError("El nombre y el apellido son obligatorios.")

        if not mail.strip() or "@" not in mail or "." not in mail:
            raise DatoInvalidoError("El mail no tiene un formato válido.")

        if any(
            usuario.mail.lower() == mail.lower()
            for usuario in self.__usuarios
        ):
            raise DuplicadoError("Ya existe un usuario con ese mail.")

        if not celular.strip():
            raise DatoInvalidoError("El celular es obligatorio.")

        if not contrasenia:
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

        if usuario_sesion.rol != Rol.ADMIN:
            raise OperacionNoPermitidaError(
                "No tenés permisos para editar usuarios."
            )

        usuario = self.buscar_por_id(id_usuario)

        if not nombre.strip() or not apellido.strip():
            raise DatoInvalidoError(
                "El nombre y el apellido son obligatorios."
            )

        if not mail.strip() or "@" not in mail or "." not in mail:
            raise DatoInvalidoError("El mail no tiene un formato válido.")

        for otro_usuario in self.__usuarios:
            if (
                otro_usuario.id != id_usuario
                and not otro_usuario.eliminado
                and otro_usuario.mail.lower() == mail.lower()
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

        if usuario_sesion.id == id_usuario:
            raise OperacionNoPermitidaError(
                "No podés eliminar tu propio usuario mientras tenés la sesión iniciada."
            )

        usuario = self.buscar_por_id(id_usuario)
        usuario.eliminar()


    def autenticar(
        self,
        mail: str,
        contrasenia: str
    ) -> Usuario:

        for usuario in self.__usuarios:
            if (
                usuario.mail.lower() == mail.lower()
                and not usuario.eliminado
                and usuario.verificar_contrasenia(contrasenia)
            ):
                return usuario

        raise CredencialesInvalidasError(
            "Mail o contraseña incorrectos."
        )