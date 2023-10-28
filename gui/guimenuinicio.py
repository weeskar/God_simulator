# guimenuinicio.py
import pygame
from widgets import ContenedorBotones

class GuiMenuInicio:

    def __init__(self, pantalla):
        # Carga la imagen de fondo.
        self.imagen_fondo = pygame.image.load('E:\\Proyectos\\god_simulator\\fondo_estrellado.png')
        self.ajustar_imagen_fondo(pantalla.get_size())
        self.salir_presionado = False
        self.opciones_presionado = False
        
        # Definimos las acciones de los botones aquí
        def accion_crear_mundo():
            print("Crear mundo presionado!")

        def accion_cargar_mundo():
            print("Cargar mundo presionado!")

        def accion_opciones():
            print("Opciones presionado!")
            self.opciones_presionado = True

        def accion_salir():
            print("Boton Salir presionado!")
            self.salir_presionado = True
        
        botones_info = [
        {"texto": "Crear Mundo", "accion": accion_crear_mundo, "pos": (100, 150)},
        {"texto": "Cargar Mundo", "accion": accion_cargar_mundo, "pos": (100, 210)},  # Cambiado de 250 a 210
        {"texto": "Opciones", "accion": accion_opciones, "pos": (100, 270)},  # Cambiado de 350 a 270
        {"texto": "Salir", "accion": accion_salir, "pos": (100, 330)},  # Cambiado de 450 a 330
        ]
        
        ancho_marco = 250
        alto_marco = 300
        
        self.contenedor_botones = ContenedorBotones(pantalla, botones_info, ancho_marco, alto_marco)
    
    def ajustar_imagen_fondo(self, size):
        """Ajusta la imagen de fondo al tamaño proporcionado."""    
        self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, size)
    
    def manejar_evento(self, evento):
        # Dejamos que el contenedor maneje el evento.
        self.contenedor_botones.manejar_evento(evento)

    def dibujar(self, pantalla):
        # Dibuja la imagen de fondo primero.
        pantalla.blit(self.imagen_fondo, (0, 0))
        # Dibuja el contenedor de botones y todos sus botones.
        self.contenedor_botones.dibujar(pantalla)