#main.py
import pygame
from pygame.locals import *
from menuinicio import mostrar_menu_inicio
from opcionesmenuinicio import OpcionesMenuInicio
from estados import EstadosJuego
import jugando  # Asumimos que la función que ejecuta el juego está aquí.

# Iniciar pygame
pygame.init()

# Constantes
ANCHO_PANTALLA = 1920
ALTO_PANTALLA = 1080
ANCHO_BOTON = 200
ALTO_BOTON = 50

# Colores
BLANCO = (255, 255, 255)

# Establecer resolución y centrar ventana
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.RESIZABLE)
pygame.display.set_caption("Simulador de Dios")

# Cargar imágenes y fuentes
fondo = pygame.image.load("e:\\Proyectos\\god_simulator\\fondo estrellado.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
fuente = pygame.font.Font(None, 36)

# Crear botones
botones = {
    "Nuevo Mundo": pygame.Rect((ANCHO_PANTALLA - ANCHO_BOTON) // 2, ALTO_PANTALLA // 2 - 100, ANCHO_BOTON, ALTO_BOTON),
    "Cargar Mundo": pygame.Rect((ANCHO_PANTALLA - ANCHO_BOTON) // 2, ALTO_PANTALLA // 2, ANCHO_BOTON, ALTO_BOTON),
    "Opciones": pygame.Rect((ANCHO_PANTALLA - ANCHO_BOTON) // 2, ALTO_PANTALLA // 2 + 100, ANCHO_BOTON, ALTO_BOTON),
    "Salir": pygame.Rect((ANCHO_PANTALLA - ANCHO_BOTON) // 2, ALTO_PANTALLA // 2 + 200, ANCHO_BOTON, ALTO_BOTON)
}

# Bucle principal del juego
ejecutando = True
estado_actual = EstadosJuego.MENU_INICIO

while ejecutando:
    if estado_actual == EstadosJuego.MENU_INICIO:
        estado_actual = mostrar_menu_inicio(pantalla, botones, fondo, fuente)
    elif estado_actual == EstadosJuego.JUGANDO:
        estado_actual = jugando.iniciar_juego(pantalla)
    elif estado_actual == EstadosJuego.OPCIONES_MENU_INICIO:
        opciones_menu_inicio = OpcionesMenuInicio(pantalla, fondo, fuente, ANCHO_PANTALLA, ALTO_PANTALLA, ANCHO_BOTON, ALTO_BOTON)
        estado_actual = opciones_menu_inicio.mostrar()
    elif estado_actual == EstadosJuego.SALIR:
        ejecutando = False

pygame.quit() 