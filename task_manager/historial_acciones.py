"""
Estructura de datos: Pila (Stack)
---------------------------------
Una pila es una estructura de datos que sigue el principio LIFO (Last In, First Out - último en entrar, primero en salir).
Es conveniente usar pilas para implementar el historial de acciones (deshacer/rehacer) porque:
1. El orden temporal de las acciones es crucial - la última acción realizada es la primera que se debe deshacer.
2. El deshacer/rehacer se modela naturalmente con operaciones push (agregar) y pop (quitar) de una pila.
3. Mantener dos pilas (deshacer y rehacer) permite navegar de forma bidireccional por el historial.
4. Las operaciones son O(1) en tiempo, lo que garantiza una respuesta instantánea al usuario.
5. El modelo mental de "apilar" acciones es intuitivo y refleja cómo los usuarios entienden la funcionalidad.
"""

class Accion:
    def __init__(self, tipo_accion, tarea, valores_antiguos=None):
        self.tipo_accion = tipo_accion  # "AGREGAR", "ELIMINAR", "ACTUALIZAR"
        self.tarea = tarea
        self.valores_antiguos = valores_antiguos  # Para guardar los valores anteriores en caso de ACTUALIZAR
        
class HistorialAcciones:
    def __init__(self):
        self.pila_deshacer = []
        self.pila_rehacer = []
        
    def agregar_accion(self, accion):
        self.pila_deshacer.append(accion)
        # Cuando se agrega una nueva acción, se limpia la pila de rehacer
        self.pila_rehacer.clear()
        
    def puede_deshacer(self):
        return len(self.pila_deshacer) > 0
        
    def puede_rehacer(self):
        return len(self.pila_rehacer) > 0
        
    def deshacer(self):
        if not self.puede_deshacer():
            return None
            
        accion = self.pila_deshacer.pop()
        self.pila_rehacer.append(accion)
        return accion
        
    def rehacer(self):
        if not self.puede_rehacer():
            return None
            
        accion = self.pila_rehacer.pop()
        self.pila_deshacer.append(accion)
        return accion 