#main.py
import pygame
from menuinicio import MenuInicio
from opcionesmenuinicio import MenuOpciones
from gestorestados import GestorEstados

class MainDelPrograma:
    def __init__(self, ancho=800, alto=600):
        # Inicialización de pygame
        pygame.init()

        # crear ventana
        self.pantalla = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
        pygame.display.set_caption("Mi Juego con Máquina de Estados")
        self.reloj = pygame.time.Clock()

        # Configuración del gestor de estados
        self.gestor_estados = GestorEstados()
        self.gestor_estados.agregar_estado("menu_inicio", MenuInicio(self.pantalla, self.gestor_estados))
        self.gestor_estados.agregar_estado("menu_opciones", MenuOpciones(self.pantalla, self.gestor_estados))
        self.gestor_estados.cambiar_estado("menu_inicio")  # Establecer un estado inicial
        
        self.ejecutando = True

    def BuclePrincipal(self):
        # Bucle principal del juego
        while self.ejecutando:
            # Procesamiento de eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

                respuesta = self.gestor_estados.manejar_evento(evento)
                if respuesta == "SALIR":
                    self.ejecutando = False
                elif respuesta == "OPCIONES":
                    self.gestor_estados.cambiar_estado("menu_opciones")

            # Actualización y dibujo
            self.gestor_estados.actualizar()
            self.gestor_estados.dibujar(self.pantalla)
            
            # Actualización de la pantalla y control de la tasa de fotogramas
            pygame.display.flip()
            self.reloj.tick(60)
        
        # Salida de pygame
        pygame.quit()

if __name__ == "__main__":
    programa = MainDelPrograma()
    programa.BuclePrincipal()