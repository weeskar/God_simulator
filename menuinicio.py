#menuinicio.py
import pygame
from estados import EstadosJuego

def mostrar_menu_inicio(pantalla, botones, fondo, fuente):
    pantalla.blit(fondo, (0, 0))
    
    # Ajuste de separación vertical entre botones
    separacion_vertical = 20
    posicion_x = pantalla.get_width() // 2 - botones["Nuevo Mundo"].width // 2
    posicion_y = pantalla.get_height() // 2 - (botones["Nuevo Mundo"].height + separacion_vertical) * (len(botones) // 2)

    for nombre, rectangulo in botones.items():
        rectangulo.x = posicion_x
        rectangulo.y = posicion_y
        if rectangulo.collidepoint(pygame.mouse.get_pos()):
            color_boton = (100, 100, 100) 
        else:
            color_boton = (50, 50, 50)

        pygame.draw.rect(pantalla, color_boton, rectangulo)
        etiqueta = fuente.render(nombre, True, (255, 255, 255))
        pantalla.blit(etiqueta, (rectangulo.x + (rectangulo.width - etiqueta.get_width()) // 2, rectangulo.y + (rectangulo.height - etiqueta.get_height()) // 2))

        posicion_y += botones["Nuevo Mundo"].height + separacion_vertical
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return EstadosJuego.SALIR
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for nombre, rectangulo in botones.items():
                if rectangulo.collidepoint(evento.pos):
                    if nombre == "Nuevo Mundo":
                        return EstadosJuego.JUGANDO
                    elif nombre == "Salir":
                        return EstadosJuego.SALIR
                    elif nombre == "Opciones":
                        return EstadosJuego.OPCIONES_MENU_INICIO
                    elif evento.type == pygame.VIDEORESIZE:  # Manejo del evento de redimensionamiento
                                fondo = pygame.transform.scale(fondo, (evento.w, evento.h))
                                posicion_x = evento.w // 2 - botones["Nuevo Mundo"].width // 2
                                posicion_y = evento.h // 2 - (botones["Nuevo Mundo"].height + separacion_vertical) * (len(botones) // 2)

    pygame.display.flip()
    return EstadosJuego.MENU_INICIO  # Si no se ha hecho clic en ningún botón, mantente en el estado del menú.