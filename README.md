# Documentación: Sistema de Gestión de Tareas

## Índice
1. [Descripción del Problema y Solución](#descripción-del-problema-y-solución)
2. [Estructuras de Datos Utilizadas](#estructuras-de-datos-utilizadas)
   - [Lista](#lista)
   - [Pila](#pila)
   - [Cola](#cola)
   - [Árbol](#árbol)
3. [Instrucciones para Compilar y Ejecutar](#instrucciones-para-compilar-y-ejecutar)
4. [Arquitectura del Sistema](#arquitectura-del-sistema)
5. [Funcionalidades Principales](#funcionalidades-principales)
6. [Guía de Uso](#guía-de-uso)
7. [Modo Demostración](#modo-demostración)
8. [Descripción de Módulos](#descripción-de-módulos)
9. [Diagrama de Clases](#diagrama-de-clases)

## Descripción del Problema y Solución

### El Problema

El problema consiste en desarrollar una aplicación de gestión de tareas para una empresa que permita a los usuarios:

1. **Mantener una lista de tareas pendientes** donde cada tarea tiene título, descripción, prioridad y fecha de vencimiento.
2. **Implementar un historial de acciones** realizadas (deshacer/rehacer) en las tareas.
3. **Gestionar una cola de tareas urgentes** que requieren atención inmediata y deben ser procesadas en el orden en que llegan.
4. **Organizar las tareas jerárquicamente** según su categoría (trabajo, personal, estudios) y subcategorías.

Este problema requiere el uso eficiente de diferentes estructuras de datos para manejar adecuadamente cada aspecto.

### La Solución

La solución implementada es un sistema de gestión de tareas completo que utiliza:

1. **Listas** para el almacenamiento general de tareas, permitiendo acceso aleatorio y ordenamiento flexible.
2. **Pilas** para implementar la funcionalidad de deshacer/rehacer, siguiendo el principio "último en entrar, primero en salir".
3. **Colas** para gestionar tareas urgentes, garantizando procesamiento en orden de llegada.
4. **Árboles** para organizar las tareas en categorías y subcategorías, facilitando la navegación jerárquica.

El sistema cuenta con una interfaz gráfica intuitiva que permite a los usuarios interactuar con todas estas funcionalidades de manera sencilla. La arquitectura modular garantiza una clara separación de responsabilidades y facilita el mantenimiento.

## Estructuras de Datos Utilizadas

### Lista

**Implementación:** `lista_tareas.py`

**Descripción:**
La lista es una estructura de datos secuencial que permite almacenar elementos en un orden específico, con acceso aleatorio a cualquier elemento por su posición o identificador.

**¿Por qué se eligió?**
- **Acceso aleatorio eficiente:** Permite buscar, consultar y modificar tareas específicas en O(n) en el peor caso.
- **Versatilidad de ordenamiento:** Facilita ordenar las tareas por diferentes criterios (prioridad, fecha) según las necesidades del usuario.
- **Operaciones sencillas:** Las operaciones de inserción y eliminación son intuitivas y de implementación directa.
- **Facilidad para recorrer elementos:** Permite iterar fácilmente por todas las tareas para mostrarlas o procesarlas.
- **Adecuada para la cantidad de datos:** Para la cantidad de tareas que normalmente maneja un usuario, una lista simple proporciona rendimiento suficiente.

**Alternativas consideradas:**
- **Array asociativo (diccionario):** Ofrecería búsqueda O(1) pero complicaría el ordenamiento.
- **Lista ligada:** Complicaría el acceso aleatorio que se necesita frecuentemente.

### Pila

**Implementación:** `historial_acciones.py`

**Descripción:**
Una pila (stack) es una estructura de datos que sigue el principio LIFO (Last In, First Out), donde el último elemento agregado es el primero en ser retirado.

**¿Por qué se eligió?**
- **Modelado natural del historial:** La metáfora de "apilar" acciones refleja cómo los usuarios entienden el historial de operaciones.
- **Operaciones O(1):** Las operaciones push (agregar) y pop (quitar) tienen tiempo constante, proporcionando respuesta inmediata.
- **Control bidireccional:** El uso de dos pilas (deshacer y rehacer) permite navegar en ambas direcciones por el historial.
- **Gestión eficiente de memoria:** Solo almacena las acciones realizadas, no estados completos.
- **Estándar en la industria:** Es la estructura recomendada para implementar funcionalidad de deshacer/rehacer.

**Alternativas consideradas:**
- **Lista con índice:** Requeriría gestión manual del índice actual y resultaría menos eficiente.
- **Árbol de estados:** Sería excesivamente complejo para esta aplicación.

### Cola

**Implementación:** `cola_urgentes.py`

**Descripción:**
Una cola (queue) es una estructura que sigue el principio FIFO (First In, First Out), donde el primer elemento agregado es el primero en ser retirado.

**¿Por qué se eligió?**
- **Orden temporal garantizado:** Asegura que las tareas urgentes se procesen en el orden en que fueron agregadas.
- **Justicia en el procesamiento:** Evita la "inanición" de tareas antiguas, garantizando que todas sean eventualmente atendidas.
- **Operaciones O(1):** Las operaciones de encolar y desencolar tienen tiempo constante.
- **Modelo mental claro:** Refleja la idea de una "lista de espera" que es intuitiva para los usuarios.
- **Implementación optimizada:** Utiliza la clase `deque` de Python que está optimizada para operaciones en ambos extremos.

**Alternativas consideradas:**
- **Lista de prioridad:** Complicaría innecesariamente el proceso, ya que todas las tareas en esta cola ya son urgentes.
- **Lista ordenada por tiempo:** No aportaría ventajas sobre una cola FIFO para este caso.

### Árbol

**Implementación:** `arbol_categorias.py`

**Descripción:**
Un árbol es una estructura de datos jerárquica donde cada nodo puede tener múltiples hijos, formando niveles y ramificaciones.

**¿Por qué se eligió?**
- **Representación natural de jerarquías:** Las categorías y subcategorías forman naturalmente una estructura de árbol.
- **Navegación intuitiva:** Facilita la navegación vertical (padre-hijo) entre categorías relacionadas.
- **Agrupación lógica:** Permite agrupar tareas relacionadas bajo una estructura organizativa que refleja la manera en que los usuarios piensan.
- **Operaciones recursivas eficientes:** Facilita operaciones como "mostrar todas las tareas en esta categoría y sus subcategorías".
- **Flexibilidad de crecimiento:** Permite añadir nuevas categorías o niveles sin reestructurar el sistema.

**Alternativas consideradas:**
- **Lista plana con prefijos:** Menos eficiente para consultas jerárquicas.
- **Grafo general:** Innecesariamente complejo para una relación puramente jerárquica.

## Instrucciones para Compilar y Ejecutar

### Requisitos Previos
- Python 3.6 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**
   ```
   git clone [url-del-repositorio]
   cd [nombre-del-directorio]
   ```
   Si no usas git, simplemente descarga y descomprime los archivos del proyecto.

2. **Instalar las dependencias**
   ```
   pip install tkcalendar
   ```
   La única dependencia externa es `tkcalendar`, que proporciona un widget de calendario para seleccionar fechas.

3. **Ejecutar la aplicación**
   ```
   python main.py
   ```
   Esto iniciará la aplicación con la interfaz gráfica.

### Modos de Ejecución

El programa ofrece varios modos de ejecución:

- **Modo normal:**
  ```
  python main.py
  ```
  Inicia la aplicación con una base de datos vacía.

- **Modo demostración (GUI):**
  ```
  python main.py --demo-gui
  ```
  Inicia la interfaz gráfica con datos de ejemplo precargados.

### Verificación de la Instalación

Para verificar que la instalación se ha completado correctamente:

1. Ejecute el programa en modo demostración:
   ```
   python main.py --demo-gui
   ```

2. Debería ver la interfaz gráfica con categorías y tareas precargadas.

3. Pruebe las diferentes funcionalidades:
   - Seleccione distintas categorías
   - Cree una nueva tarea
   - Marque una tarea como completada
   - Pruebe el deshacer/rehacer

Si todo funciona correctamente, la instalación ha sido exitosa.

## Arquitectura del Sistema

El sistema sigue una arquitectura modular organizada en capas:

1. **Capa de Modelo:** Contiene las clases fundamentales que representan los datos.
   - `models.py`: Define las clases `Tarea` y `Prioridad`.

2. **Capa de Estructuras de Datos:** Implementa las estructuras específicas.
   - `lista_tareas.py`: Implementa la lista de tareas.
   - `historial_acciones.py`: Implementa las pilas para deshacer/rehacer.
   - `cola_urgentes.py`: Implementa la cola para tareas urgentes.
   - `arbol_categorias.py`: Implementa el árbol para categorías.

3. **Capa de Lógica de Negocio:** Coordina las operaciones del sistema.
   - `gestor_tareas.py`: Gestor central que coordina todas las operaciones.

4. **Capa de Presentación:** Maneja la interfaz con el usuario.
   - `interfaz_grafica.py`: Implementa la interfaz gráfica con Tkinter.

5. **Utilidades:**
   - `demo_datos.py`: Proporciona datos de demostración.
   - `main.py`: Punto de entrada principal.

## Funcionalidades Principales

### Gestión de Tareas
- Crear nuevas tareas con título, descripción, prioridad y fecha de vencimiento
- Editar tareas existentes
- Eliminar tareas
- Marcar tareas como completadas
- Organizar tareas en categorías

### Gestión de Categorías
- Crear categorías y subcategorías
- Organizar las tareas dentro de una estructura jerárquica
- Visualizar todas las tareas de una categoría y sus subcategorías

### Historial y Deshacer/Rehacer
- Registrar todas las acciones realizadas (agregar, editar, eliminar)
- Deshacer la última acción realizada
- Rehacer acciones previamente deshechas
- Visualizar el historial completo de acciones

### Tareas Urgentes
- Cola especial para tareas con prioridad urgente
- Procesamiento ordenado de tareas urgentes

## Guía de Uso

### Ventana Principal

La interfaz del programa se divide en varias secciones:

1. **Panel de Categorías (izquierda):**
   - Muestra la estructura jerárquica de categorías
   - Permite navegar entre categorías y subcategorías
   - El botón "Nueva Categoría" permite crear categorías nuevas

2. **Panel de Tareas (derecha):**
   - Muestra las tareas de la categoría seleccionada
   - Las tareas se muestran con su prioridad, título, fecha y estado
   - Los botones permiten crear, editar, eliminar y completar tareas
   - También incluye botones para deshacer y rehacer acciones

3. **Panel de Historial (abajo):**
   - Muestra un registro de las acciones realizadas
   - Indica cuántas acciones se pueden deshacer o rehacer

4. **Panel de Tareas Urgentes (abajo):**
   - Muestra las tareas marcadas como urgentes
   - Permite procesar la siguiente tarea urgente en la cola

### Crear una Tarea

1. Seleccione la categoría donde desea crear la tarea (opcional)
2. Haga clic en "Nueva Tarea"
3. Complete el formulario con:
   - Título (obligatorio)
   - Descripción
   - Prioridad (Baja, Media, Alta, Urgente)
   - Fecha de vencimiento
   - Categoría
4. Haga clic en "Guardar"

### Organizar por Categorías

Las categorías se organizan jerárquicamente. Para crear una subcategoría:

1. Seleccione la categoría padre
2. Haga clic en "Nueva Categoría"
3. Introduzca el nombre de la subcategoría

### Usar el Historial

- Para deshacer la última acción: Haga clic en "Deshacer"
- Para rehacer una acción deshecha: Haga clic en "Rehacer"
- Para ver todas las acciones: Observe el panel de historial

### Gestionar Tareas Urgentes

Las tareas marcadas como "Urgente" se añaden automáticamente a la cola de tareas urgentes.

1. Vea las tareas urgentes en el panel inferior
2. Haga clic en "Procesar" para marcar como completada la tarea urgente más antigua

## Modo Demostración

El sistema incluye un modo de demostración que carga datos de ejemplo para mostrar las funcionalidades:

- **Modo GUI:** Inicia la interfaz gráfica con datos precargados.
  ```
  python main.py --demo-gui
  ```

La demostración incluye:
- Una estructura jerárquica de categorías
- Tareas de ejemplo con diferentes prioridades y fechas
- Ejemplos de cada estructura de datos en acción

## Descripción de Módulos

### models.py
Define las clases fundamentales:
- `Prioridad`: Enumeración para los niveles de prioridad (BAJA, MEDIA, ALTA, URGENTE)
- `Tarea`: Representa una tarea con propiedades como título, descripción, prioridad, etc.

### lista_tareas.py
Implementa la estructura de lista para la gestión de tareas:
- Agregar, eliminar, actualizar tareas
- Ordenar tareas por diferentes criterios
- Búsqueda de tareas específicas

### historial_acciones.py
Implementa las pilas para el historial de acciones:
- Registrar acciones (agregar, eliminar, actualizar)
- Deshacer/rehacer acciones
- Gestionar el estado de las pilas

### cola_urgentes.py
Implementa la cola para tareas urgentes:
- Agregar tareas urgentes
- Procesar la siguiente tarea urgente
- Visualizar todas las tareas en la cola

### arbol_categorias.py
Implementa el árbol para las categorías:
- Crear y navegar por categorías jerárquicas
- Asignar tareas a categorías
- Obtener todas las tareas de una categoría y sus subcategorías

### gestor_tareas.py
Coordina todas las operaciones del sistema:
- Gestión central de tareas, categorías, historial y cola
- Implementa las operaciones de alto nivel como crear tareas
- Coordina la interacción entre las diferentes estructuras

### interfaz_grafica.py
Implementa la interfaz gráfica de usuario:
- Visualización y gestión de tareas
- Navegación por categorías
- Interacción con todas las funcionalidades del sistema

### demo_datos.py
Proporciona datos de ejemplo para demostraciones:
- Crea una estructura de categorías y subcategorías
- Agrega tareas de ejemplo
- Incluye funciones para mostrar estadísticas y ejemplos

## Diagrama de Clases

```
+---------------+       +---------------+       +----------------+
|    Tarea      |       | ListaTareas   |       | GestorTareas   |
+---------------+       +---------------+       +----------------+
| - id          |       | - tareas      |       | - lista_tareas |
| - titulo      | <---- | + agregar()   | <---- | - historial    |
| - descripcion |       | + eliminar()  |       | - cola_urgentes|
| - prioridad   |       | + obtener()   |       | - arbol_categ. |
| - fecha_venc. |       | + actualizar()|       | + crear_tarea()|
| - categoria   |       | + ordenar()   |       | + eliminar()   |
| - completada  |       +---------------+       | + actualizar() |
+---------------+                               | + deshacer()   |
                                                | + rehacer()    |
                                                +----------------+
                                                       ^
                                                       |
+-----------------+      +----------------+     +---------------+
| HistorialAcciones|     | ColaTareasUrg. |     | ArbolCategorias|
+-----------------+      +----------------+     +---------------+
| - pila_deshacer |      | - cola         |     | - raiz        |
| - pila_rehacer  |      | + agregar()    |     | + agregar()   |
| + agregar()     |      | + procesar()   |     | + buscar()    |
| + deshacer()    |      | + ver_sig()    |     | + agregar_tarea|
| + rehacer()     |      | + esta_vacia() |     | + obtener()   |
+-----------------+      +----------------+     +---------------+
```

