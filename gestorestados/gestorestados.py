
#gestorestados.py
class GestorEstados:
    def __init__(self):
        self.estados = {}  # Un diccionario para almacenar los estados por nombre o clave.
        self.estado_actual = None
        self.estado_anterior = None
    
    def agregar_estado(self, nombre, estado):
        """Agrega un estado al gestor."""
        self.estados[nombre] = estado

    def cambiar_estado(self, nombre):
        """Cambia el estado actual solo si es diferente del estado actual."""
        if self.estado_actual != self.estados.get(nombre):
            self.estado_anterior = self.estado_actual  # Guarda el estado actual antes de cambiarlo.
            self.estado_actual = self.estados.get(nombre)
    
    def cambiar_estado_anterior(self):
        """Cambia al estado anterior."""
        if self.estado_anterior:
            self.estado_actual, self.estado_anterior = self.estado_anterior, self.estado_actual

    def manejar_evento(self, evento):
        """Delega el manejo del evento al estado actual."""
        if self.estado_actual:
            return self.estado_actual.manejar_evento(evento)
            

    def actualizar(self):
        """Actualiza el estado actual."""
        if self.estado_actual:
            self.estado_actual.actualizar()

    def dibujar(self, pantalla):
        """Dibuja el estado actual."""
        if self.estado_actual:
            self.estado_actual.dibujar(pantalla)

# Clase base para todos los estados del juego.
class EstadoJuego:
    def __init__(self):
        """
        Constructor base para inicializar cualquier recurso que puedan necesitar todos los estados.
        En algunos casos, puede que no necesites inicializar nada en la clase base. La palabra clave
        `pass` en Python se usa como una declaración nula. Es decir, cuando es ejecutada, no ocurre nada.
        Se usa generalmente como un marcador de posición.

        """
        pass

    def manejar_evento(self, evento):
        """
        Este método se encarga de manejar eventos como pulsaciones de teclas o clics del mouse.
        En la clase base, a menudo no sabes exactamente cómo debe manejar eventos un estado particular,
        pero sabes que cada estado debe tener la capacidad de manejarlos. Por eso, defines un método
        de marcador de posición con `pass` para que las subclases lo sobrescriban con comportamientos 
        específicos.
        """
        pass

    def actualizar(self):
        """
        Método para actualizar cualquier lógica o recurso asociado a un estado.
        Igual que antes, la implementación exacta depende de cada subclase, por lo que aquí solo se 
        coloca como marcador de posición.
        """
        pass

    def dibujar(self, pantalla):
        """
        Método para dibujar elementos visuales en la pantalla.
        De nuevo, el comportamiento específico depende del estado actual, por lo que en la clase base
        simplemente usamos `pass`.
        """
        pass

    