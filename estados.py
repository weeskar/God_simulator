#estados.py
from enum import Enum

class EstadosJuego(Enum):
    MENU_INICIO = "menu_inicio"
    OPCIONES_MENU_INICIO = "opciones_menu_inicio"
    JUGANDO = "jugando"
    SALIR = "salir"
    MENU_OPCIONES_JUGANDO = "menu_opciones_jugando"  # Agrega esta línea