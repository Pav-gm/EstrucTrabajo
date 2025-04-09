from datetime import datetime
from .models import Tarea, Prioridad

"""
Estructura de datos: Lista
----------------------------
La lista es una estructura de datos secuencial que permite almacenar elementos en un orden específico.
Es conveniente usar listas para la gestión de tareas porque:
1. Permite acceso aleatorio a los elementos, facilitando la búsqueda y modificación de tareas específicas.
2. El orden de inserción se mantiene, lo que es útil para reconstruir el historial de creación de tareas.
3. Facilita operaciones como ordenar las tareas por diferentes criterios (prioridad, fecha).
4. La flexibilidad para agregar o eliminar elementos en cualquier posición.
5. Implementación sencilla y eficiente para colecciones de tamaño moderado.
"""

class ListaTareas:
    def __init__(self):
        self.tareas = []
        
    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)
        return tarea
    
    def eliminar_tarea(self, tarea_id):
        for i, tarea in enumerate(self.tareas):
            if tarea.id == tarea_id:
                return self.tareas.pop(i)
        return None
    
    def obtener_tarea(self, tarea_id):
        for tarea in self.tareas:
            if tarea.id == tarea_id:
                return tarea
        return None
    
    def actualizar_tarea(self, tarea_id, **kwargs):
        tarea = self.obtener_tarea(tarea_id)
        if tarea:
            tarea.actualizar(**kwargs)
            return tarea
        return None
    
    def obtener_todas_tareas(self):
        return self.tareas.copy()
    
    def ordenar_por_prioridad(self):
        return sorted(self.tareas, key=lambda t: (t.prioridad.value, t.fecha_vencimiento), reverse=True)
    
    def ordenar_por_fecha(self):
        return sorted(self.tareas, key=lambda t: t.fecha_vencimiento) 