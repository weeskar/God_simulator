#guimenuopciones.py
import pygame
from widgets import Boton, ContenedorBotones

# Puedes ajustar las dimensiones de los botones según tus preferencias.
ancho_marco_botones_opciones = 200
alto_marco_botones_opciones = 200
MARGEN = 10

class GuiMenuOpciones:
    def __init__(self, pantalla, gestor_estados):
        # Carga una imagen de fondo (si lo deseas).
     
        
        # Definimos las acciones de los botones aquí
        def accion_resolucion():
            print("Cambiar resolución presionado!")

        def accion_volumen():
            print("Control de volumen presionado!")

        botones_info = [
            {"texto": "Resolución", "accion": accion_resolucion},
            {"texto": "Volumen", "accion": accion_volumen}
        ]
        self.contenedor_botones = ContenedorBotones(pantalla, botones_info, ancho_marco_botones_opciones, alto_marco_botones_opciones)
        self.boton_volver = BotonVolver(pantalla, self.volver)
   
    def volver(self):
        # Aquí cambiamos al estado anterior almacenado en el gestor de estados.
        self.cambio_estado_anterior()
   
    def manejar_evento(self, evento):
        self.contenedor_botones.manejar_evento(evento)
        self.boton_volver.manejar_evento(evento)
    
    def dibujar(self, pantalla):
        pantalla.fill((0, 0, 0))  # Rellenar la pantalla con negro.
        self.contenedor_botones.dibujar(pantalla)
        self.boton_volver.dibujar(pantalla)

class BotonVolver:
    def __init__(self, pantalla, gestor_estados, ancho=150, alto=50, color=(50, 50, 50), color_hover=(100, 100, 100)):
        self.pantalla = pantalla
        self.ancho = ancho  # Almacenamos ancho
        self.alto = alto  # Almacenamos alto
        self.boton = Boton(0, 0, ancho, alto, "Volver", self.cambiar_pulsado, color, color_hover)
        self.actualizar_posicion()  # Esta función ahora usa self.ancho y self.alto
        self.pulsado = False  # Esta es la variable que nos dirá si el botón ha sido pulsado
        self.gestor_estados = gestor_estados
    
    def cambiar_pulsado(self):
        """ Esta función será llamada cuando se pulse el botón. """
        self.pulsado = True

    def actualizar_posicion(self):
        ancho_pantalla, alto_pantalla = self.pantalla.get_size()
        self.x = ancho_pantalla - self.ancho - MARGEN
        self.y = alto_pantalla - self.alto - MARGEN
        self.boton.rect.topleft = (self.x, self.y)

    def manejar_evento(self, evento):
        if self.boton.manejar_evento(evento) and evento.type == pygame.MOUSEBUTTONDOWN:
            self.cambiar_pulsado()

    def dibujar(self, pantalla):
        self.boton.dibujar(pantalla)