#opcionesmenuinicio.py
import pygame
from guimenuopciones import GuiMenuOpciones,BotonVolver, MARGEN # Este importa el GUI para opciones.
from gestorestados import EstadoJuego
from widgets import ContenedorBotones,Boton

class MenuOpciones(EstadoJuego):
    
    def __init__(self, pantalla, gestor_estados):
        super().__init__()
        self.contenedor_botones = ContenedorBotones(pantalla, botones_info, ancho_marco_botones_opciones, alto_marco_botones_opciones)
        self.boton_volver = BotonVolver(pantalla, gestor_estados)
    
    def manejar_evento(self, evento):
        self.gui_menu_opciones.manejar_evento(evento)
        # Para manejar el redimensionamiento:
        if evento.type == pygame.VIDEORESIZE:
            self.gui_menu_opciones.boton_volver.actualizar_posicion()
            self.dibujar(self.pantalla)  # Redibujamos todo.
    
    def volver(self):
        self.gestor_estados.cambiar_estado_anterior()
    
    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        self.gui_menu_opciones.dibujar(pantalla)
