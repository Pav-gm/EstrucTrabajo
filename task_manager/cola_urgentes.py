from collections import deque

"""
Estructura de datos: Cola (Queue)
---------------------------------
Una cola es una estructura de datos que sigue el principio FIFO (First In, First Out - primero en entrar, primero en salir).
Es conveniente usar colas para manejar tareas urgentes porque:
1. Garantiza que las tareas se procesen en el orden en que fueron agregadas, respetando la prioridad temporal.
2. Modela naturalmente una lista de espera, donde la próxima tarea a procesar es siempre la que lleva más tiempo esperando.
3. Operaciones de encolar (append) y desencolar (popleft) son O(1), asegurando alto rendimiento.
4. Previene que tareas antiguas sean ignoradas indefinidamente, evitando el "starvation" (inanición).
5. La implementación deque de Python ofrece una solución optimizada con operaciones eficientes en ambos extremos.
"""

class ColaTareasUrgentes:
    def __init__(self):
        self.cola = deque()
        
    def agregar_tarea(self, tarea):
        self.cola.append(tarea)
        
    def procesar_siguiente(self):
        if not self.esta_vacia():
            return self.cola.popleft()
        return None
        
    def ver_siguiente(self):
        if not self.esta_vacia():
            return self.cola[0]
        return None
        
    def esta_vacia(self):
        return len(self.cola) == 0
        
    def tamaño(self):
        return len(self.cola)
        
    def obtener_todas(self):
        return list(self.cola) 