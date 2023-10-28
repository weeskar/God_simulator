# Clase para el estado del menú de inicio del juego.
#menuinicio.py

import pygame
from guimenuinicio import GuiMenuInicio
from gestorestados import EstadoJuego

class MenuInicio(EstadoJuego):
    def __init__(self, pantalla, gestor_estados):
        super().__init__()  # Llamamos al constructor de la clase base.
        self.gui_menu_inicio = GuiMenuInicio(pantalla)  # Creamos una instancia de GUIInicio para manejar la interfaz gráfica del menú.
        
    def manejar_evento(self, evento):
        # Para este estado, queremos manejar eventos específicos, así que sobrescribimos el método.
        
        # Primero, dejamos que la interfaz gráfica del menú maneje el evento.
        # Esto podría incluir cosas como detectar si se ha hecho clic en un botón.
        self.gui_menu_inicio.manejar_evento(evento)
      
        # Detectamos si el botón de salir fue presionado
        if self.gui_menu_inicio.salir_presionado:
            return "SALIR"
        
        if self.gui_menu_inicio.opciones_presionado:
            return "OPCIONES"

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                # Aquí es donde podrías cambiar al siguiente estado, si lo deseas.
                pass
        if evento.type == pygame.VIDEORESIZE:
                
                # Actualiza la imagen de fondo al nuevo tamaño de pantalla.
                self.gui_menu_inicio.ajustar_imagen_fondo((evento.w, evento.h))
                # Actualiza la posición del contenedor de botones y otros elementos relevantes.
                self.gui_menu_inicio.contenedor_botones.actualizar_posicion()
    
    def actualizar(self):
        # Si hubiera alguna lógica específica que quisieras actualizar regularmente para este estado,
        # la colocarías aquí. En este caso, no hay ninguna lógica específica para actualizar, así que 
        # el método no hace nada.
        pass

    def dibujar(self, pantalla):
        # Dibujamos la interfaz gráfica del menú en la pantalla.
        # Este método se encarga de mostrar todos los elementos visuales del menú, como botones.
        self.gui_menu_inicio.dibujar(pantalla)



