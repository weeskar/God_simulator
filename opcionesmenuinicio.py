#opcionesmenuinicio.py
import pygame
from estados import EstadosJuego

# Constantes
ESPACIO_BOTON = 50
ANCHO_BOTON_RESOLUCION = 200


class OpcionesMenuInicio:

    def __init__(self, pantalla, fondo, fuente, ANCHO, ALTO, ANCHO_BOTON, ALTO_BOTON):
        self.fullscreen = False
        self.pantalla = pantalla
        self.fondo = fondo
        self.fuente = fuente
        self.ANCHO = ANCHO
        self.ALTO = ALTO
        self.ANCHO_BOTON = ANCHO_BOTON
        self.ALTO_BOTON = ALTO_BOTON
        self.boton_volver = pygame.Rect((self.ANCHO - self.ANCHO_BOTON) // 2,
                                        self.ALTO - self.ALTO_BOTON * 4,
                                        self.ANCHO_BOTON, self.ALTO_BOTON)
        self.resoluciones = ["800x600", "1024x768", "1280x720", "1366x768", "1600x900", "1920x1080", "2560x1440",
                             "3840x2160"]
        self.resolucion_actual = 5
        self.opciones = {
            "Opciones de Video": [
                ("Resolución", "1920x1080"),
                ("Modo Ventana", False),
                ("V-Sync", True),
                ("Anti-Aliasing", True),
            ],
            "Opciones de Sonido": [
                ("Volumen Principal", 80),
                ("Volumen Efectos", 70),
                ("Volumen Música", 90),
            ],
            "Otras Opciones": [
                ("Subtítulos", True),
                ("Dificultad", "Normal"),
            ]
        }
        self.opcion_activa = None

    def mostrar(self):
        while True:
            self.pantalla.blit(self.fondo, (0, 0))
            self.dibujar_opciones()
            self.dibujar_boton_volver()
            if not self.manejar_eventos():
                break
        return EstadosJuego.MENU_INICIO

    def dibujar_opciones(self):
        espaciado = self.ALTO // (len(self.opciones) + 2)
        ancho_columna = self.ANCHO // len(self.opciones)

        for indice, (categoria, items) in enumerate(self.opciones.items()):
            y = espaciado
            x = ancho_columna * indice + (ancho_columna - self.fuente.render(categoria, True, (255, 255, 255)).get_width()) // 2

            self.pantalla.blit(self.fuente.render(categoria, True, (255, 255, 255)), (x, y))
            y += 30

            for item, valor in items:
                color = (255, 255, 255) if (categoria, item) != self.opcion_activa else (255, 0, 0)
                texto = f"{item}: {valor}"
                if item == "Resolución":
                    texto = f"{item}: < {valor} >"
                self.pantalla.blit(self.fuente.render(texto, True, color), (x, y))
                y += 30

    def dibujar_boton_volver(self):
        color_boton = (70, 70, 70) if self.boton_volver.collidepoint(pygame.mouse.get_pos()) else (50, 50, 50)
        pygame.draw.rect(self.pantalla, color_boton, self.boton_volver)
        texto_volver = self.fuente.render("Volver", True, (255, 255, 255))
        self.pantalla.blit(texto_volver, (self.boton_volver.x + (self.boton_volver.width - texto_volver.get_width()) // 2,
                                          self.boton_volver.y + (self.boton_volver.height - texto_volver.get_height()) // 2))

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    self.toggle_modo_ventana()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_volver.collidepoint(evento.pos):
                    return False
                self.manejar_evento_click(evento)
            
            if evento.type == pygame.VIDEORESIZE:
                self.ANCHO, self.ALTO = evento.size
                self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO), pygame.RESIZABLE)
                self.boton_volver = pygame.Rect((self.ANCHO - self.ANCHO_BOTON) // 2,
                                                self.ALTO - self.ALTO_BOTON * 4,
                                                self.ANCHO_BOTON, self.ALTO_BOTON)
        pygame.display.flip()
        return True

    def manejar_evento_click(self, evento):
        espaciado = self.ALTO // (len(self.opciones) + 2)
        ancho_columna = self.ANCHO // len(self.opciones)

        for columna, (cat, items) in enumerate(self.opciones.items()):
            y = espaciado + 30
            x = ancho_columna * columna + 200

            for i, (opcion, valor) in enumerate(items):
                rect_opcion = pygame.Rect(x, y, self.ANCHO // 3 - 100, 30)
                if rect_opcion.collidepoint(evento.pos):
                    self.opcion_activa = (cat, opcion)
                    self.toggle_opcion(i, cat, opcion, valor)
                y += 30

    def toggle_opcion(self, i, cat, opcion, valor):
        opciones_funciones = {
            "Resolución": self.cambiar_resolucion,
            "Modo Ventana": self.toggle_modo_ventana
        }

        if opcion in opciones_funciones:
            if opcion == "Resolución":
                opciones_funciones[opcion](i)
            else:
                opciones_funciones[opcion]()
        elif isinstance(valor, bool):
            lista_opciones = self.opciones[cat]
            lista_opciones[i] = (opcion, not valor)
            self.opciones[cat] = lista_opciones
        
    def cambiar_resolucion(self, i):
        lista_opciones = self.opciones["Opciones de Video"]

        resolucion_anterior = self.resoluciones[self.resolucion_actual]

        # Cambia a la siguiente resolución
        if self.resolucion_actual < len(self.resoluciones) - 1:
            self.resolucion_actual += 1
        else:
            self.resolucion_actual = 0

        nueva_resolucion = self.resoluciones[self.resolucion_actual]
        self.pantalla = pygame.display.set_mode(nueva_resolucion, pygame.RESIZABLE)
        lista_opciones[i] = ("Resolución", nueva_resolucion)
        self.opciones["Opciones de Video"] = lista_opciones

        # Comienza la cuenta regresiva para confirmar
        tiempo_inicio = pygame.time.get_ticks()
        while True:
            if pygame.time.get_ticks() - tiempo_inicio > 15000:  # 15 segundos
                self.pantalla = pygame.display.set_mode(resolucion_anterior, pygame.RESIZABLE)
                break
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    return  # Confirma la nueva resolución

    def toggle_modo_ventana(self):
        if self.fullscreen:
            self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        else:
            self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO), pygame.FULLSCREEN)
        self.fullscreen = not self.fullscreen