from datetime import datetime, timedelta
from .models import Prioridad, Tarea
from .gestor_tareas import GestorTareas

def cargar_datos_demo(gestor=None):
    """
    Carga datos de demostración en el gestor de tareas.
    Si no se proporciona un gestor, crea uno nuevo.
    
    Returns:
        GestorTareas: El gestor con datos de ejemplo cargados
    """
    if gestor is None:
        gestor = GestorTareas()
    
    # Crear estructura de categorías (Demostración del Árbol)
    print("Creando estructura de categorías...")
    gestor.arbol_categorias.agregar_categoria("Trabajo")
    gestor.arbol_categorias.agregar_categoria("Trabajo/Proyecto A")
    gestor.arbol_categorias.agregar_categoria("Trabajo/Proyecto A/Fase 1")
    gestor.arbol_categorias.agregar_categoria("Trabajo/Proyecto A/Fase 2")
    gestor.arbol_categorias.agregar_categoria("Trabajo/Proyecto B")
    gestor.arbol_categorias.agregar_categoria("Personal")
    gestor.arbol_categorias.agregar_categoria("Personal/Salud")
    gestor.arbol_categorias.agregar_categoria("Personal/Finanzas")
    gestor.arbol_categorias.agregar_categoria("Estudios")
    gestor.arbol_categorias.agregar_categoria("Estudios/Universidad")
    gestor.arbol_categorias.agregar_categoria("Estudios/Cursos Online")
    
    # Crear tareas con diferentes prioridades y fechas (Demostración de Lista)
    print("Agregando tareas de ejemplo...")
    
    # Fechas para las tareas
    hoy = datetime.now()
    manana = hoy + timedelta(days=1)
    proxima_semana = hoy + timedelta(days=7)
    proximo_mes = hoy + timedelta(days=30)
    
    # Tareas de trabajo
    gestor.crear_tarea(
        "Reunión de equipo", 
        "Preparar presentación para la reunión semanal de equipo", 
        Prioridad.ALTA, 
        manana, 
        "Trabajo/Proyecto A/Fase 1"
    )
    
    gestor.crear_tarea(
        "Entregar informe trimestral", 
        "Completar y enviar el informe de resultados del trimestre", 
        Prioridad.URGENTE, 
        manana, 
        "Trabajo/Proyecto A"
    )
    
    gestor.crear_tarea(
        "Revisar documentación", 
        "Revisar la documentación técnica del proyecto", 
        Prioridad.MEDIA, 
        proxima_semana, 
        "Trabajo/Proyecto A/Fase 1"
    )
    
    gestor.crear_tarea(
        "Planificar desarrollo", 
        "Crear cronograma de desarrollo para la fase 2", 
        Prioridad.MEDIA, 
        proximo_mes, 
        "Trabajo/Proyecto A/Fase 2"
    )
    
    gestor.crear_tarea(
        "Enviar propuesta", 
        "Preparar y enviar propuesta para el nuevo cliente", 
        Prioridad.ALTA, 
        manana, 
        "Trabajo/Proyecto B"
    )
    
    # Tareas personales
    gestor.crear_tarea(
        "Cita médica", 
        "Acudir a la revisión anual", 
        Prioridad.MEDIA, 
        proxima_semana, 
        "Personal/Salud"
    )
    
    gestor.crear_tarea(
        "Revisar gastos", 
        "Actualizar registro de gastos del mes", 
        Prioridad.BAJA, 
        proxima_semana, 
        "Personal/Finanzas"
    )
    
    gestor.crear_tarea(
        "Pagar facturas", 
        "Pagar facturas de servicios antes del vencimiento", 
        Prioridad.URGENTE, 
        manana, 
        "Personal/Finanzas"
    )
    
    # Tareas de estudios
    gestor.crear_tarea(
        "Entregar trabajo final", 
        "Completar y enviar el trabajo final del curso", 
        Prioridad.ALTA, 
        proxima_semana, 
        "Estudios/Universidad"
    )
    
    gestor.crear_tarea(
        "Clase de Python", 
        "Asistir a la clase online de Python avanzado", 
        Prioridad.MEDIA, 
        manana, 
        "Estudios/Cursos Online"
    )
    
    # Devolver el gestor con los datos cargados
    return gestor


def mostrar_estadisticas(gestor):
    """
    Muestra estadísticas y ejemplos del sistema para demostrar cada estructura de datos
    """
    print("\n" + "="*50)
    print("DEMOSTRACIÓN DEL GESTOR DE TAREAS")
    print("="*50)
    
    # 1. DEMOSTRACIÓN DE LISTAS
    print("\n--- DEMOSTRACIÓN DE LISTAS ---")
    print("Tareas ordenadas por prioridad:")
    for i, tarea in enumerate(gestor.lista_tareas.ordenar_por_prioridad()):
        print(f"{i+1}. {tarea}")
    
    print("\nTareas ordenadas por fecha:")
    for i, tarea in enumerate(gestor.lista_tareas.ordenar_por_fecha()):
        print(f"{i+1}. {tarea.titulo} - {tarea.fecha_vencimiento.strftime('%d/%m/%Y')}")
    
    # 2. DEMOSTRACIÓN DE PILAS (HISTORIAL)
    print("\n--- DEMOSTRACIÓN DE PILAS (HISTORIAL) ---")
    print(f"Acciones en historial: {len(gestor.historial_acciones.pila_deshacer)}")
    print(f"Se puede deshacer: {'Sí' if gestor.historial_acciones.puede_deshacer() else 'No'}")
    print(f"Se puede rehacer: {'Sí' if gestor.historial_acciones.puede_rehacer() else 'No'}")
    
    print("\nDeshaciendo la última acción:")
    if gestor.deshacer():
        print("  Acción deshecha correctamente")
    
    print("Rehaciendo la acción:")
    if gestor.rehacer():
        print("  Acción rehecha correctamente")
    
    # 3. DEMOSTRACIÓN DE COLAS (TAREAS URGENTES)
    print("\n--- DEMOSTRACIÓN DE COLAS (TAREAS URGENTES) ---")
    tareas_urgentes = gestor.cola_urgentes.obtener_todas()
    print(f"Tareas urgentes en cola: {len(tareas_urgentes)}")
    
    for i, tarea in enumerate(tareas_urgentes):
        print(f"{i+1}. {tarea.titulo}")
    
    if not gestor.cola_urgentes.esta_vacia():
        print("\nProcesando la próxima tarea urgente:")
        tarea = gestor.procesar_siguiente_urgente()
        print(f"  Tarea procesada: {tarea.titulo}")
    
    # 4. DEMOSTRACIÓN DE ÁRBOLES (CATEGORÍAS)
    print("\n--- DEMOSTRACIÓN DE ÁRBOLES (CATEGORÍAS) ---")
    print("Estructura jerárquica de categorías:")
    
    categorias = gestor.obtener_todas_categorias()
    for ruta, nodo, profundidad in categorias:
        print(f"{'  ' * profundidad}|- {nodo.nombre} ({len(nodo.tareas)} tareas)")
    
    # Mostrar tareas de una categoría específica
    categoria_ejemplo = "Trabajo/Proyecto A"
    print(f"\nTareas en la categoría '{categoria_ejemplo}':")
    tareas_categoria = gestor.obtener_tareas_por_categoria(categoria_ejemplo)
    
    for i, tarea in enumerate(tareas_categoria):
        print(f"{i+1}. {tarea.titulo}")
    
    print("\n" + "="*50)
    print("FIN DE LA DEMOSTRACIÓN")
    print("="*50)


def ejecutar_demo():
    """Ejecuta una demostración completa del sistema"""
    print("Iniciando demostración del Gestor de Tareas...\n")
    
    # Cargar datos de ejemplo
    gestor = cargar_datos_demo()
    
    # Mostrar estadísticas y ejemplos
    mostrar_estadisticas(gestor)
    
    print("\nLa demostración ha finalizado.")
    print("Puede continuar usando la aplicación con estos datos cargados.")
    
    return gestor


if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, ejecutar la demo
    ejecutar_demo() 