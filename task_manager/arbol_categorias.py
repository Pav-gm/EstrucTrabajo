"""
Estructura de datos: Árbol (Tree)
---------------------------------
Un árbol es una estructura de datos jerárquica donde cada nodo puede tener múltiples hijos.
Es conveniente usar árboles para organizar categorías porque:
1. Representa naturalmente relaciones jerárquicas (categorías y subcategorías).
2. Permite navegar fácilmente entre niveles (subir a categorías padres o bajar a subcategorías).
3. Facilita operaciones como buscar todas las tareas en una categoría y sus subcategorías.
4. La estructura refleja la organización mental que los usuarios tienen de sus tareas.
5. Las operaciones de búsqueda son eficientes, especialmente cuando el árbol está bien balanceado.
6. Permite agregar nuevas categorías en cualquier nivel sin reestructurar todo el sistema.
"""

class NodoCategoria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
        self.tareas = []
        
    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)
        return nodo_hijo
        
    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)
        
    def eliminar_tarea(self, tarea):
        if tarea in self.tareas:
            self.tareas.remove(tarea)
            return True
        return False
        
    def buscar_hijo(self, nombre):
        for hijo in self.hijos:
            if hijo.nombre == nombre:
                return hijo
        return None
        
    def __str__(self):
        return self.nombre

class ArbolCategorias:
    def __init__(self):
        self.raiz = NodoCategoria("Raíz")
        
    def agregar_categoria(self, ruta):
        """Agrega una categoría siguiendo una ruta como 'Trabajo/Proyecto A/Fase 1'"""
        partes = ruta.split('/')
        actual = self.raiz
        
        for parte in partes:
            hijo = actual.buscar_hijo(parte)
            if not hijo:
                hijo = actual.agregar_hijo(NodoCategoria(parte))
            actual = hijo
            
        return actual
        
    def buscar_categoria(self, ruta):
        """Encuentra una categoría siguiendo una ruta"""
        print(f"Buscando categoría con ruta: '{ruta}'")  # Depuración
        
        # Si la ruta es vacía, None o "todas", manejarlo adecuadamente
        if not ruta:
            return None
        
        if ruta == "todas":
            return None  # Caso especial para "todas"
        
        # Dividir la ruta en partes y comenzar desde la raíz
        partes = ruta.split('/')
        actual = self.raiz
        
        # Si la primera parte es vacía, es porque la ruta comienza con '/'
        if partes and partes[0] == '':
            partes = partes[1:]  # Omitir la primera parte vacía
        
        for parte in partes:
            if not parte:  # Saltar partes vacías
                continue
            
            print(f"  Buscando parte: '{parte}'")  # Depuración
            hijo = actual.buscar_hijo(parte)
            if not hijo:
                print(f"  No se encontró hijo '{parte}'")  # Depuración
                return None
            actual = hijo
        
        print(f"  Encontrada categoría: {actual.nombre}")  # Depuración
        return actual
        
    def agregar_tarea_a_categoria(self, tarea, ruta):
        print(f"Intentando agregar tarea '{tarea.titulo}' a categoría '{ruta}'")  # Depuración
        categoria = self.buscar_categoria(ruta)
        if categoria:
            print(f"Categoría encontrada: {categoria.nombre}")  # Depuración
            # Primero verificamos si la tarea ya estaba en otra categoría
            if tarea.categoria and tarea.categoria != ruta:
                # Intentar eliminar de la categoría anterior
                cat_anterior = self.buscar_categoria(tarea.categoria)
                if cat_anterior:
                    print(f"Eliminando tarea de categoría anterior: {tarea.categoria}")  # Depuración
                    cat_anterior.eliminar_tarea(tarea)
            
            # Agregar a la nueva categoría
            categoria.agregar_tarea(tarea)
            tarea.categoria = ruta  # Asegurarse de establecer la ruta completa como categoría
            print(f"Tarea añadida a categoría '{ruta}', tarea.categoria = '{tarea.categoria}'")  # Depuración
            return True
        
        print(f"Categoría no encontrada: '{ruta}'")  # Depuración
        return False
        
    def obtener_todas_categorias(self):
        resultado = []
        
        def recorrer(nodo, profundidad=0, ruta=""):
            # Determinar la ruta actual
            if nodo == self.raiz:
                ruta_actual = ""  # La raíz no tiene ruta
            else:
                ruta_actual = ruta + "/" + nodo.nombre if ruta else nodo.nombre
            
            # Agregar nodo actual al resultado, excepto la raíz
            if nodo != self.raiz:
                resultado.append((ruta_actual, nodo, profundidad))
            
            # Recorrer hijos
            for hijo in nodo.hijos:
                recorrer(hijo, profundidad + 1, ruta_actual)
                
        recorrer(self.raiz)
        return resultado 

    def obtener_todas_tareas_categoria(self, ruta):
        """
        Obtiene todas las tareas de una categoría y sus subcategorías recursivamente.
        
        Args:
            ruta: Ruta de la categoría
            
        Returns:
            Lista de tareas de la categoría y todas sus subcategorías
        """
        print(f"Obteniendo todas las tareas para categoría: '{ruta}'")
        categoria = self.buscar_categoria(ruta)
        if not categoria:
            print(f"  Categoría '{ruta}' no encontrada")
            return []
            
        # Recolectar todas las tareas recursivamente
        todas_tareas = []
        
        def recolectar_tareas(nodo):
            # Agregar tareas de este nodo
            todas_tareas.extend(nodo.tareas)
            print(f"  Agregadas {len(nodo.tareas)} tareas de '{nodo.nombre}'")
            
            # Recursivamente agregar tareas de los hijos
            for hijo in nodo.hijos:
                recolectar_tareas(hijo)
                
        # Comenzar recolección
        recolectar_tareas(categoria)
        print(f"  Total de tareas encontradas: {len(todas_tareas)}")
        return todas_tareas 