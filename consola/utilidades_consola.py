# ==================================================
# UTILIDADES DE CONSOLA - FOOD STORE
# Programación II - UTN FRM
# ==================================================

import os
import questionary
from colorama import Fore, Style, init

# Inicialización de Colorama
init(autoreset=True)


# ==================================================
# LIMPIEZA DE CONSOLA
# ==================================================

def limpiar_consola() -> None:
    os.system("cls" if os.name == "nt" else "clear")


# ==================================================
# PRESENTACIÓN DE MENSAJES
# ==================================================

def mostrar_titulo(titulo: str) -> None:
    print(Fore.CYAN + Style.BRIGHT)
    print("=" * 50)
    print(titulo.center(50))
    print("=" * 50)


def mostrar_exito(mensaje: str) -> None:
    print(Fore.GREEN + Style.BRIGHT + f"\n✓ {mensaje}")


def mostrar_error(mensaje: str) -> None:
    print(Fore.RED + Style.BRIGHT + f"\n✗ {mensaje}")


def mostrar_aviso(mensaje: str) -> None:
    print(Fore.YELLOW + Style.BRIGHT + f"\n! {mensaje}")


# ==================================================
# PAUSA DE CONSOLA
# ==================================================

def pausar() -> None:
    input("\nPresioná Enter para continuar...")


# ==================================================
# MENÚS INTERACTIVOS
# ==================================================

def mostrar_menu(titulo: str, opciones: list[str]) -> str | None:
    return questionary.select(
        titulo,
        choices=opciones,
        pointer="➤",
        style=questionary.Style([
            ("question", "bold"),
            ("pointer", "fg:cyan bold"),
            ("highlighted", "fg:cyan bold"),
            ("selected", "fg:green"),
        ])
    ).ask()

