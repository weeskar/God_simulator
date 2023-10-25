#jugando.py
import pygame
import random
from estados import EstadosJuego
from pygame import Rect

MAX_PARTICULAS = 150
UMBRAL_VELOCIDAD_FUSION = 1.5  # Establece un umbral para la fusión basado en la velocidad.
MARGEN = 10  # Define cuánto se desplazará una partícula fuera del borde antes de cambiar de dirección   

class Nodo:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.particulas = []
        self.children = []
        
    def contiene(self, particula):
        return (self.x <= particula.x <= self.x + self.width and
                self.y <= particula.y <= self.y + self.height)
        
    def dividir(self):
        w, h = self.width / 2, self.height / 2
        self.children = [
            Nodo(self.x, self.y, w, h), 
            Nodo(self.x + w, self.y, w, h), 
            Nodo(self.x, self.y + h, w, h), 
            Nodo(self.x + w, self.y + h, w, h)
        ]

class QuadTree:
    MAX_PROFUNDIDAD = 5  # Profundidad máxima para dividir el QuadTree
    
    def __init__(self, x, y, w, h, capacidad, profundidad=0):
        self.root = Nodo(x, y, w, h)
        self.capacidad = capacidad
        self.profundidad = profundidad
    
    def insertar(self, nodo, particula):
        if not nodo.contiene(particula):
            return False
        
        if len(nodo.particulas) < self.capacidad:
            nodo.particulas.append(particula)
            return True
        else:
            # Si estamos en una profundidad máxima, simplemente agregamos la partícula
            if self.profundidad >= self.MAX_PROFUNDIDAD:
                nodo.particulas.append(particula)
                return True

            if not nodo.children:
                nodo.dividir()

            for child in nodo.children:
                if self.insertar(child, particula):
                    return True
        return False
    
    def consultar(self, nodo, rango, resultado):
        if not self.intersecta(nodo, rango):
            return
        
        for particula in nodo.particulas:
            if rango.collidepoint(particula.x, particula.y):
                resultado.append(particula)
        
        if nodo.children:
            for child in nodo.children:
                self.consultar(child, rango, resultado)
    
    def intersecta(self, nodo, rango):
        return not (rango.x > nodo.x + nodo.width or
                    rango.x + rango.width < nodo.x or
                    rango.y > nodo.y + nodo.height or
                    rango.y + rango.height < nodo.y)

class Camara:
    NIVELES_ZOOM = [0.5, 0.75, 1, 1.5, 2]
    nivel_zoom_actual = 2
    ACELERACION_PASO = 0.4  
    FRENADO = 0.98  
    
    def __init__(self, ancho, alto, x=0, y=0):
        self.x = x
        self.y = y
        self.zoom = self.NIVELES_ZOOM[self.nivel_zoom_actual]
        self.ancho = ancho
        self.alto = alto
        self.velocidad = pygame.Vector2(0, 0)
        self.aceleracion = pygame.Vector2(0, 0)
        self.direccion = pygame.Vector2(0, 0)  

    def actualizar(self):
        if self.direccion.length() > 0:
            self.aceleracion = self.direccion.normalize() * self.ACELERACION_PASO
        else:
            self.aceleracion = pygame.Vector2(0, 0)

        self.velocidad += self.aceleracion
        self.velocidad *= self.FRENADO
        self.x += self.velocidad.x
        self.y += self.velocidad.y

        self.x = min(max(0, self.x), self.ancho - self.ancho / self.zoom)
        self.y = min(max(0, self.y), self.alto - self.alto / self.zoom)

    def aplicar(self, x, y):
        return int((x - self.x) * self.zoom), int((y - self.y) * self.zoom)

    def mover(self, dx, dy):
        self.x += dx / self.zoom
        self.y += dy / self.zoom

    def ajustar_zoom(self, direccion, mouse_pos):
        zoom_previo = self.zoom

        if direccion == "acercar" and self.nivel_zoom_actual < len(self.NIVELES_ZOOM) - 1:
            self.nivel_zoom_actual += 1
        elif direccion == "alejar" and self.nivel_zoom_actual > 0:
            self.nivel_zoom_actual -= 1

        self.zoom = self.NIVELES_ZOOM[self.nivel_zoom_actual]
        
        # Calculamos el factor de cambio de escala
        scale_factor = self.zoom / zoom_previo

        # Calculamos el nuevo centro de zoom
        self.x = (mouse_pos[0] - self.x) * scale_factor + self.x
        self.y = (mouse_pos[1] - self.y) * scale_factor + self.y

        # Si estamos en el nivel más alejado de zoom, centrar la cámara
        if self.zoom == self.NIVELES_ZOOM[0]: 
            self.x = (self.ancho - self.ancho / self.zoom) / 2
            self.y = (self.alto - self.alto / self.zoom) / 2

        # Limitar la posición para asegurarnos de que no estamos fuera del mapa
        self.x = min(max(0, self.x), self.ancho - self.ancho / self.zoom)
        self.y = min(max(0, self.y), self.alto - self.alto / self.zoom)

    def procesar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key in [pygame.K_UP, pygame.K_w]:
                self.direccion.y = -1
            elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                self.direccion.y = 1
            elif evento.key in [pygame.K_LEFT, pygame.K_a]:
                self.direccion.x = -1
            elif evento.key in [pygame.K_RIGHT, pygame.K_d]:
                self.direccion.x = 1
        elif evento.type == pygame.KEYUP:
            if evento.key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                self.direccion.y = 0
            if evento.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                self.direccion.x = 0
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4:  
                self.ajustar_zoom("acercar", evento.pos)
            elif evento.button == 5:  
                self.ajustar_zoom("alejar", evento.pos)

class GestorCapas:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.capa_actual = CapaEstelar(pantalla)  # Inicializamos con la capa estelar

    def cambiar_capa(self, nueva_capa):
        self.capa_actual = nueva_capa

    def main(self):
        ejecutando = True
        while ejecutando:
            eventos = pygame.event.get()
            estado = self.capa_actual.procesar_eventos(eventos)
            if estado == EstadosJuego.SALIR:
                return estado

            self.capa_actual.actualizar()
            self.capa_actual.dibujar()

        return None  # Retorna a otro estado del juego, por ejemplo, el menú principal

class Particula:
    MAX_VELOCIDAD = 0.5
    DISTANCIA_MAX_ATRACCION = 100
    PROBABILIDAD_LIBERAR_ENERGIA = 0.1
    ZONA_AMORTIGUACION = 50  # definimos una zona de 50 píxeles cerca del borde
    FUERZA_AMORTIGUACION = 0.05  # esto determina cuán fuerte es el empuje hacia el centro
    COLORES_TIPOS = {
        "hidrogeno": (173, 216, 230),
        "helio": (0, 255, 0),
        "estrella": (255, 255, 0),
        "default": (255, 255, 255)
    }


    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad_x = random.uniform(-self.MAX_VELOCIDAD, self.MAX_VELOCIDAD)  # Aumento de la velocidad inicial
        self.velocidad_y = random.uniform(-self.MAX_VELOCIDAD, self.MAX_VELOCIDAD)  # Aumento de la velocidad inicial
        self.masa = random.uniform(0.5, 2)
        self.radio = self.masa  # Reducción del tamaño inicial
        self.fuerza_atraccion = self.masa * 0.05
        self.tiempo_efecto_fusion = 0
        self.encendida = True  # Por defecto, la partícula estará "encendida"

    def obtener_velocidad(self):
        return (self.velocidad_x**2 + self.velocidad_y**2) ** 0.5

    def fusionar(self, particula):
        mayor = self if self.masa > particula.masa else particula
        menor = particula if mayor is self else self

        nueva_masa = mayor.masa + menor.masa

        mayor.x = (mayor.x * mayor.masa + menor.x * menor.masa) / nueva_masa
        mayor.y = (mayor.y * mayor.masa + menor.y * menor.masa) / nueva_masa
        mayor.radio += menor.radio
        mayor.masa = nueva_masa
        mayor.tiempo_efecto_fusion = 20  # Ajustamos el efecto de fusión en la partícula "mayor".

        if self.tipo == "hidrogeno" and particula.tipo == "hidrogeno":  # Manejo de fusiones
            mayor.tipo = "helio"
        elif self.tipo == "helio" and particula.tipo == "helio":  # Manejo de fusiones
            mayor.tipo = "carbono"
        # Puedes agregar más condiciones aquí

        menor.eliminado = True  # Marcar la partícula "menor" para eliminación.

    def dibujar(self, pantalla, camara):
        # Inicialmente, establece el color en blanco
        color = (255, 255, 255) 

        # Si el tiempo del efecto de fusión es positivo, selecciona un color de fusión
        if self.tiempo_efecto_fusion > 0:
            colores_fusion = [(255, 255, 0), (255, 0, 0), (128, 0, 128), (173, 216, 230)]
            color = random.choice(colores_fusion)
            self.tiempo_efecto_fusion -= 1
            # Alterna entre encendida y apagada para el efecto de destello
            self.encendida = not self.encendida
        else:
            colores_tipo = {
                "helio": (0, 255, 0),        # Verde
                "hidrogeno": (173, 216, 230), # Azul claro
                "estrella": (255, 255, 0)    # Amarillo
            }
            color = colores_tipo.get(self.tipo, color) # Si no hay coincidencia en el diccionario, se mantiene blanco

            # Asegúrate de que esté encendida fuera del efecto
            self.encendida = True  

        x_pantalla, y_pantalla = camara.aplicar(self.x, self.y)
        if self.encendida:
            pygame.draw.circle(pantalla, color, (x_pantalla, y_pantalla), int(self.radio * camara.zoom))

    def mover(self, ancho_pantalla, alto_pantalla):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

        # Aplicar la fuerza de amortiguación para el borde horizontal
        if 0 < self.x < self.ZONA_AMORTIGUACION:
            self.velocidad_x += self.FUERZA_AMORTIGUACION * (self.ZONA_AMORTIGUACION - self.x) / self.ZONA_AMORTIGUACION
        elif ancho_pantalla - self.ZONA_AMORTIGUACION < self.x < ancho_pantalla:
            self.velocidad_x -= self.FUERZA_AMORTIGUACION * (self.x - ancho_pantalla + self.ZONA_AMORTIGUACION) / self.ZONA_AMORTIGUACION

        # Aplicar la fuerza de amortiguación para el borde vertical
        if 0 < self.y < self.ZONA_AMORTIGUACION:
            self.velocidad_y += self.FUERZA_AMORTIGUACION * (self.ZONA_AMORTIGUACION - self.y) / self.ZONA_AMORTIGUACION
        elif alto_pantalla - self.ZONA_AMORTIGUACION < self.y < alto_pantalla:
            self.velocidad_y -= self.FUERZA_AMORTIGUACION * (self.y - alto_pantalla + self.ZONA_AMORTIGUACION) / self.ZONA_AMORTIGUACION

        # Ajustes opcionales para garantizar que las partículas no salgan de la pantalla:
        self.x = max(min(self.x, ancho_pantalla), 0)
        self.y = max(min(self.y, alto_pantalla), 0)

    
    def atraer(self, particulas_cercanas, quadtree):
        quadtree.consultar(quadtree.root, pygame.Rect(self.x, self.y, self.DISTANCIA_MAX_ATRACCION * 2, self.DISTANCIA_MAX_ATRACCION * 2), particulas_cercanas)

        # Buscar partículas cercanas con QuadTree
        for particula in particulas_cercanas:
            if particula is not self:
                dx = particula.x - self.x
                dy = particula.y - self.y
                distancia = max(1, (dx*dx + dy*dy) ** 0.5)

                if distancia < self.DISTANCIA_MAX_ATRACCION:
                    fuerza = (self.fuerza_atraccion * particula.fuerza_atraccion) / (distancia ** 2)

                    self.velocidad_x += (dx / distancia) * fuerza
                    self.velocidad_y += (dy / distancia) * fuerza

class CapaEstelar:
    
    RADIO_CERCANIA = 10  # Valor arbitrario para definir cercanía entre partículas
    FACTOR_DISTANCIA_FUSION = 0.2  # Multiplicador para la suma de radios en fusión
    
    def __init__(self, pantalla):
            
            self.pantalla = pantalla
            self.ancho_pantalla = pantalla.get_width()
            self.alto_pantalla = pantalla.get_height()
            self.camara = Camara(self.ancho_pantalla, self.alto_pantalla)
            self.particulas = [Particula(random.randrange(0, self.ancho_pantalla),
                                        random.randrange(0, self.alto_pantalla),
                                        "hidrogeno" if random.randrange(0, 2) == 0 else "helio")
                            for _ in range(100)]

    def procesar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                return EstadosJuego.SALIR
            else:
                self.camara.procesar_evento(evento)
        return EstadosJuego.JUGANDO
   
    def actualizar(self):
       # Construcción del QuadTree:
        limite_pantalla = Rect(0, 0, self.pantalla.get_width(), self.pantalla.get_height())
        quadtree = QuadTree(limite_pantalla.x, limite_pantalla.y, limite_pantalla.width, limite_pantalla.height, 4)
        for particula in self.particulas:
            quadtree.insertar(quadtree.root, particula)

        particulas_a_eliminar = set()

        for i, particula in enumerate(self.particulas):
            particula.mover(self.ancho_pantalla, self.alto_pantalla)

            rango_cercano = Rect(particula.x - self.RADIO_CERCANIA, particula.y - self.RADIO_CERCANIA, 2 * self.RADIO_CERCANIA, 2 * self.RADIO_CERCANIA)
            
            cercanas = []
            quadtree.consultar(quadtree.root, rango_cercano, cercanas)
            
            particula.atraer(cercanas, quadtree)
            
            for j, particula_cercana in enumerate(cercanas):
                if j <= i:
                    continue
                
                distancia = pygame.math.Vector2(particula.x, particula.y).distance_to(pygame.math.Vector2(particula_cercana.x, particula_cercana.y))
                distancia_fusion = self.FACTOR_DISTANCIA_FUSION * (particula.radio + particula_cercana.radio)

                if distancia < distancia_fusion:
                    particula.fusionar(particula_cercana)
                    particulas_a_eliminar.add(j)

        for i in sorted(particulas_a_eliminar, reverse=True):
            del self.particulas[i]

        if len(self.particulas) < MAX_PARTICULAS:
            for particula in self.particulas[:]:
                if random.random() < Particula.PROBABILIDAD_LIBERAR_ENERGIA:
                    for _ in range(3):
                        nueva_particula = Particula(particula.x + random.randint(-5, 5),
                                                    particula.y + random.randint(-5, 5),
                                                    random.choice(["hidrogeno", "helio"]))
                        nueva_particula.masa = 0.2
                        nueva_particula.radio = 0.3
                        self.particulas.append(nueva_particula)

        # Actualización de la cámara:
        self.camara.actualizar()

    def dibujar(self):
        self.pantalla.fill((0, 0, 0))
        for particula in self.particulas:
            particula.dibujar(self.pantalla, self.camara)
        pygame.display.flip()

def iniciar_juego(pantalla):
    gestor = GestorCapas(pantalla)
    return gestor.main()