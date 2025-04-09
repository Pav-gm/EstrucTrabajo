from datetime import datetime
from .models import Tarea, Prioridad
from .lista_tareas import ListaTareas
from .historial_acciones import Accion, HistorialAcciones
from .cola_urgentes import ColaTareasUrgentes
from .arbol_categorias import ArbolCategorias

class GestorTareas:
    def __init__(self):
        self.lista_tareas = ListaTareas()
        self.historial_acciones = HistorialAcciones()
        self.cola_urgentes = ColaTareasUrgentes()
        self.arbol_categorias = ArbolCategorias()
        
        # Crear algunas categorías predeterminadas
        self.arbol_categorias.agregar_categoria("Trabajo")
        self.arbol_categorias.agregar_categoria("Personal")
        self.arbol_categorias.agregar_categoria("Estudios")
        
    def crear_tarea(self, titulo, descripcion, prioridad, fecha_vencimiento, categoria=None):
        # Asegurar que fecha_vencimiento sea datetime
        if hasattr(fecha_vencimiento, 'date') and callable(getattr(fecha_vencimiento, 'date')):
            # Ya es un datetime, no hacer nada
            pass
        elif hasattr(fecha_vencimiento, 'year'):
            # Es un date, convertir a datetime
            fecha_vencimiento = datetime.combine(fecha_vencimiento, datetime.min.time())
        
        tarea = Tarea(titulo, descripcion, prioridad, fecha_vencimiento)
        
        # Agregar a la lista general
        self.lista_tareas.agregar_tarea(tarea)
        
        # Registrar acción
        self.historial_acciones.agregar_accion(Accion("AGREGAR", tarea))
        
        # Agregar a la categoría si se especificó
        if categoria:
            self.arbol_categorias.agregar_tarea_a_categoria(tarea, categoria)
            
        # Si es urgente, añadir a la cola de urgentes
        if prioridad == Prioridad.URGENTE:
            self.cola_urgentes.agregar_tarea(tarea)
            
        return tarea
        
    def eliminar_tarea(self, tarea_id):
        tarea = self.lista_tareas.obtener_tarea(tarea_id)
        if tarea:
            # Eliminar de la lista general
            self.lista_tareas.eliminar_tarea(tarea_id)
            
            # Registrar acción
            self.historial_acciones.agregar_accion(Accion("ELIMINAR", tarea))
            
            # No es necesario eliminar explícitamente de la cola de urgentes
            # ya que las referencias seguirán apuntando al objeto
            
            return tarea
        return None
        
    def actualizar_tarea(self, tarea_id, **kwargs):
        tarea = self.lista_tareas.obtener_tarea(tarea_id)
        if tarea:
            # Guardar valores antiguos para poder deshacer
            valores_antiguos = {
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'prioridad': tarea.prioridad,
                'fecha_vencimiento': tarea.fecha_vencimiento,
                'categoria': tarea.categoria
            }
            
            # Actualizar la tarea
            resultado = self.lista_tareas.actualizar_tarea(tarea_id, **kwargs)
            
            # Registrar acción
            self.historial_acciones.agregar_accion(Accion("ACTUALIZAR", tarea, valores_antiguos))
            
            # Verificar si es urgente para añadir a la cola
            if tarea.prioridad == Prioridad.URGENTE and valores_antiguos['prioridad'] != Prioridad.URGENTE:
                self.cola_urgentes.agregar_tarea(tarea)
                
            return resultado
        return None
        
    def deshacer(self):
        if not self.historial_acciones.puede_deshacer():
            return False
            
        accion = self.historial_acciones.deshacer()
        
        if accion.tipo_accion == "AGREGAR":
            # Deshacer una adición es eliminar
            self.lista_tareas.eliminar_tarea(accion.tarea.id)
            
        elif accion.tipo_accion == "ELIMINAR":
            # Deshacer una eliminación es añadir de nuevo
            self.lista_tareas.agregar_tarea(accion.tarea)
            
        elif accion.tipo_accion == "ACTUALIZAR":
            # Deshacer una actualización es restaurar los valores antiguos
            tarea = self.lista_tareas.obtener_tarea(accion.tarea.id)
            if tarea:
                tarea.actualizar(**accion.valores_antiguos)
                
        return True
        
    def rehacer(self):
        if not self.historial_acciones.puede_rehacer():
            return False
            
        accion = self.historial_acciones.rehacer()
        
        if accion.tipo_accion == "AGREGAR":
            # Rehacer una adición es añadir de nuevo
            self.lista_tareas.agregar_tarea(accion.tarea)
            
        elif accion.tipo_accion == "ELIMINAR":
            # Rehacer una eliminación es eliminar
            self.lista_tareas.eliminar_tarea(accion.tarea.id)
            
        elif accion.tipo_accion == "ACTUALIZAR":
            # Rehacer una actualización
            # Para simplificar, solo dejamos que la tarea siga con sus valores actuales
            pass
            
        return True
        
    def procesar_siguiente_urgente(self):
        return self.cola_urgentes.procesar_siguiente()
        
    def obtener_todas_categorias(self):
        return self.arbol_categorias.obtener_todas_categorias()
        
    def obtener_tareas_por_categoria(self, ruta_categoria):
        print(f"Buscando tareas en categoría: '{ruta_categoria}'")  # Depuración
        
        # Caso especial para "todas" o cuando no hay categoría seleccionada
        if not ruta_categoria or ruta_categoria == "todas":
            print("Devolviendo todas las tareas (categoría especial)")
            return self.lista_tareas.obtener_todas_tareas()
        
        # Usar el método recursivo para obtener todas las tareas de la categoría y sus subcategorías
        return self.arbol_categorias.obtener_todas_tareas_categoria(ruta_categoria) 