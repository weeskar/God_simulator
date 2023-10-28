#widgets.py
import pygame
ancho_marco_botones_inicio = 200
alto_marco_botones_inicio = 300
MARGEN = 10  # Margen a cada lado del botón

class ContenedorBotones:
    def __init__(self, pantalla, botones_info, ancho_marco, alto_marco, color_fondo=(50, 50, 50), color_boton=(50, 50, 50), color_boton_hover=(100, 100, 100)):
        self.pantalla = pantalla
        self.botones = []
        self.ancho_marco = ancho_marco
        self.alto_marco = alto_marco
        self.color_fondo = color_fondo
        self.color_boton = color_boton
        self.color_boton_hover = color_boton_hover
        
        self.crear_botones(botones_info)
        self.actualizar_posicion()

    def crear_botones(self, botones_info):
        ancho_boton = self.ancho_marco - (2 * MARGEN)

        # Calcula la altura del botón basado en el alto total del marco y la cantidad de botones
        altura_boton = (self.alto_marco - ((len(botones_info) + 1) * MARGEN)) / len(botones_info)

        for info in botones_info:
            boton = Boton(0, 0, ancho_boton, altura_boton, info["texto"], info["accion"], self.color_boton, self.color_boton_hover)
            self.botones.append(boton)
            
    def actualizar_posicion(self):
        # Centra el contenedor en función del tamaño actual de la pantalla.
        ancho_pantalla, alto_pantalla = self.pantalla.get_size()
        x = (ancho_pantalla - self.ancho_marco) // 2  
        y = (alto_pantalla - self.alto_marco) // 2  
        self.x = x
        self.y = y
        
        # Ajustamos la posición de cada botón para que estén centrados en el contenedor.
        espaciado_botones = (self.alto_marco - (len(self.botones) * 50)) // (len(self.botones) + 0.5)
        # El espaciado ahora solo es el margen, ya que los botones se ajustan al contenedor
        for i, boton in enumerate(self.botones):
            boton.rect.topleft = (self.x + MARGEN, self.y + i * (boton.rect.height + MARGEN))

    def manejar_evento(self, evento):
        for boton in self.botones:
            boton.manejar_evento(evento)

    def dibujar(self, pantalla):
        # Ajustamos el fondo del contenedor
       # fondo_rect = pygame.Rect(self.x, self.y, self.ancho_marco, self.alto_marco)
       # pygame.draw.rect(pantalla, self.color_fondo, fondo_rect)
        
        # Dibuja los botones
        for boton in self.botones:
            boton.dibujar(pantalla)


class Boton:
    def __init__(self, x, y, ancho, alto, texto, accion, color=(50, 50, 50), color_hover=(100, 100, 100), fuente=None, tamano_fuente=32, color_texto=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.color_actual = self.color
        self.accion = accion  # Guardamos la acción que el botón realizará.
        self.fuente = pygame.font.Font(fuente, tamano_fuente)  # Permitimos personalizar la fuente y su tamaño
        self.color_texto = color_texto

    def manejar_evento(self, evento):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color_actual = self.color_hover
            if evento.type == pygame.MOUSEBUTTONDOWN:
                self.accion() 
        else:
            self.color_actual = self.color

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color_actual, self.rect)
        lbl = self.fuente.render(self.texto, True, self.color_texto)
        pantalla.blit(lbl, (self.rect.x + (self.rect.width - lbl.get_width()) // 2, 
                            self.rect.y + (self.rect.height - lbl.get_height()) // 2))
