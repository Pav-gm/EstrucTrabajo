import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkcalendar
from datetime import datetime
from .models import Prioridad
from .gestor_tareas import GestorTareas

class InterfazGrafica:
    def __init__(self, root, gestor=None):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        self.gestor_tareas = gestor if gestor else GestorTareas()
        
        # Variables para almacenar selecciones
        self.tarea_seleccionada = None
        self.categoria_seleccionada = None
        
        self._crear_widgets()
        self._configurar_estilos()
        self._actualizar_listas()
        self._actualizar_historial()
    
    def _configurar_estilos(self):
        # Configurar estilos
        estilo = ttk.Style()
        estilo.configure("TFrame", background="#f0f0f0")
        estilo.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        estilo.configure("TButton", font=('Arial', 10))
        estilo.configure("Heading.TLabel", font=('Arial', 12, 'bold'))
        
        # Estilos para prioridades
        estilo.configure("Baja.TLabel", foreground="green")
        estilo.configure("Media.TLabel", foreground="blue")
        estilo.configure("Alta.TLabel", foreground="orange")
        estilo.configure("Urgente.TLabel", foreground="red")
    
    def _crear_widgets(self):
        # Frame principal dividido en dos secciones verticales
        self.panel_principal_v = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.panel_principal_v.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel superior para categorías y tareas
        self.panel_superior = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.panel_principal_v.add(self.panel_superior, weight=3)
        
        # Panel izquierdo para categorías
        self.panel_izquierdo = ttk.Frame(self.panel_superior)
        self.panel_superior.add(self.panel_izquierdo, weight=1)
        
        # Panel derecho para tareas
        self.panel_derecho = ttk.Frame(self.panel_superior)
        self.panel_superior.add(self.panel_derecho, weight=3)
        
        # Panel inferior para historial de acciones
        self.panel_historial = ttk.LabelFrame(self.panel_principal_v, text="Historial de Acciones")
        self.panel_principal_v.add(self.panel_historial, weight=1)
        
        # Categorías
        ttk.Label(self.panel_izquierdo, text="Categorías", style="Heading.TLabel").pack(anchor="w", padx=5, pady=5)
        
        # Botones para categorías
        frame_botones_cat = ttk.Frame(self.panel_izquierdo)
        frame_botones_cat.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(frame_botones_cat, text="Nueva Categoría", command=self._nueva_categoria).pack(side=tk.LEFT, padx=2)
        
        # Treeview para categorías
        self.tree_categorias = ttk.Treeview(self.panel_izquierdo)
        self.tree_categorias.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree_categorias.heading("#0", text="Categorías")
        self.tree_categorias.bind("<<TreeviewSelect>>", self._seleccionar_categoria)
        
        # Tareas
        ttk.Label(self.panel_derecho, text="Tareas", style="Heading.TLabel").pack(anchor="w", padx=5, pady=5)
        
        # Botones para tareas
        frame_botones_tareas = ttk.Frame(self.panel_derecho)
        frame_botones_tareas.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(frame_botones_tareas, text="Nueva Tarea", command=self._nueva_tarea).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones_tareas, text="Editar", command=self._editar_tarea).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones_tareas, text="Eliminar", command=self._eliminar_tarea).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones_tareas, text="Completar", command=self._completar_tarea).pack(side=tk.LEFT, padx=2)
        
        # Botones de deshacer/rehacer
        ttk.Button(frame_botones_tareas, text="Historial", command=self._actualizar_historial).pack(side=tk.RIGHT, padx=2)
        ttk.Button(frame_botones_tareas, text="Deshacer", command=self._deshacer).pack(side=tk.RIGHT, padx=2)
        ttk.Button(frame_botones_tareas, text="Rehacer", command=self._rehacer).pack(side=tk.RIGHT, padx=2)
        
        # Lista de tareas
        self.frame_tareas = ttk.Frame(self.panel_derecho)
        self.frame_tareas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columnas = ("prioridad", "titulo", "vencimiento", "estado")
        self.tree_tareas = ttk.Treeview(self.frame_tareas, columns=columnas, show="headings")
        self.tree_tareas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.frame_tareas, orient="vertical", command=self.tree_tareas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tareas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar columnas
        self.tree_tareas.heading("prioridad", text="Prioridad")
        self.tree_tareas.heading("titulo", text="Título")
        self.tree_tareas.heading("vencimiento", text="Vencimiento")
        self.tree_tareas.heading("estado", text="Estado")
        
        self.tree_tareas.column("prioridad", width=100)
        self.tree_tareas.column("titulo", width=300)
        self.tree_tareas.column("vencimiento", width=150)
        self.tree_tareas.column("estado", width=100)
        
        self.tree_tareas.bind("<<TreeviewSelect>>", self._seleccionar_tarea)
        self.tree_tareas.bind("<Double-1>", lambda event: self._editar_tarea())
        
        # Configuración del panel de historial
        frame_historial_acciones = ttk.Frame(self.panel_historial)
        frame_historial_acciones.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # TreeView para mostrar el historial
        columnas_historial = ("indice", "accion", "tarea", "detalles")
        self.tree_historial = ttk.Treeview(frame_historial_acciones, columns=columnas_historial, show="headings", height=5)
        self.tree_historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Barra de desplazamiento para el historial
        scrollbar_historial = ttk.Scrollbar(frame_historial_acciones, orient="vertical", command=self.tree_historial.yview)
        scrollbar_historial.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_historial.configure(yscrollcommand=scrollbar_historial.set)
        
        # Configurar columnas del historial
        self.tree_historial.heading("indice", text="#")
        self.tree_historial.heading("accion", text="Acción")
        self.tree_historial.heading("tarea", text="Tarea")
        self.tree_historial.heading("detalles", text="Detalles")
        
        self.tree_historial.column("indice", width=40)
        self.tree_historial.column("accion", width=100)
        self.tree_historial.column("tarea", width=200)
        self.tree_historial.column("detalles", width=400)
        
        # Panel de información y botones de historial
        frame_info_historial = ttk.Frame(self.panel_historial)
        frame_info_historial.pack(fill=tk.X, padx=5, pady=5)
        
        self.lbl_total_acciones = ttk.Label(frame_info_historial, text="Total de acciones: 0")
        self.lbl_total_acciones.pack(side=tk.LEFT, padx=5)
        
        self.lbl_total_rehacer = ttk.Label(frame_info_historial, text="Acciones para rehacer: 0")
        self.lbl_total_rehacer.pack(side=tk.LEFT, padx=5)
        
        # Barra de estado
        self.barra_estado = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Panel de tareas urgentes
        self.frame_urgentes = ttk.LabelFrame(self.root, text="Tareas Urgentes")
        self.frame_urgentes.pack(fill=tk.X, padx=5, pady=5, before=self.barra_estado)
        
        self.lista_urgentes = tk.Listbox(self.frame_urgentes, height=3)
        self.lista_urgentes.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT, expand=True)
        
        ttk.Button(self.frame_urgentes, text="Procesar", 
                   command=self._procesar_urgente).pack(padx=5, pady=5, side=tk.RIGHT)
    
    def _actualizar_listas(self):
        # Actualizar árbol de categorías
        self.tree_categorias.delete(*self.tree_categorias.get_children())
        
        # Insertar categoría "Todas"
        self.tree_categorias.insert("", "end", text="Todas", iid="todas")
        
        # Obtener todas las categorías ordenadas por profundidad para asegurar que los padres se creen antes que los hijos
        categorias = sorted(self.gestor_tareas.obtener_todas_categorias(), key=lambda x: x[2])
        
        # Insertar cada categoría directamente con su ruta completa como ID
        for ruta, nodo, profundidad in categorias:
            # Asegurarnos de que nunca intentamos usar "Raíz" como ID
            if nodo.nombre == "Raíz":
                continue
            
            # Para categorías de primer nivel, el padre es la raíz del árbol (cadena vacía "")
            if profundidad == 0:
                self.tree_categorias.insert("", "end", text=nodo.nombre, iid=ruta)
            else:
                # Para subcategorías, calcular el ID del padre
                partes = ruta.split('/')
                padre = '/'.join(partes[:-1])  # El padre es la ruta sin el último segmento
                
                # Verificar que el padre existe antes de intentar insertar
                try:
                    self.tree_categorias.insert(padre, "end", text=nodo.nombre, iid=ruta)
                except Exception as e:
                    print(f"Error al insertar categoría '{ruta}': {e}")
                    # Intentar insertar en la raíz como fallback
                    self.tree_categorias.insert("", "end", text=nodo.nombre, iid=ruta)
        
        # Actualizar lista de tareas según la categoría seleccionada
        self._actualizar_tareas()
        
        # Actualizar lista de tareas urgentes
        self.lista_urgentes.delete(0, tk.END)
        for tarea in self.gestor_tareas.cola_urgentes.obtener_todas():
            self.lista_urgentes.insert(tk.END, tarea.titulo)
    
    def _actualizar_tareas(self):
        # Limpiar lista actual
        self.tree_tareas.delete(*self.tree_tareas.get_children())
        
        # Depuración
        print(f"Actualizando tareas para categoría: {self.categoria_seleccionada}")
        
        # Obtener tareas según la categoría seleccionada
        if not self.categoria_seleccionada or self.categoria_seleccionada == "todas":
            tareas = self.gestor_tareas.lista_tareas.obtener_todas_tareas()
            print(f"Mostrando todas las tareas: {len(tareas)}")
        else:
            tareas = self.gestor_tareas.obtener_tareas_por_categoria(self.categoria_seleccionada)
            print(f"Tareas para {self.categoria_seleccionada}: {len(tareas)}")
        
        # Si no hay tareas, salir
        if not tareas:
            print("No hay tareas para mostrar")
            return
        
        # Ordenar por prioridad
        try:
            tareas = sorted(tareas, key=lambda t: (
                t.prioridad.value, 
                t.fecha_vencimiento.strftime("%Y%m%d") if hasattr(t.fecha_vencimiento, 'strftime') else str(t.fecha_vencimiento)
            ), reverse=True)
        except Exception as e:
            print(f"Error al ordenar tareas: {e}")
        
        # Insertar en la lista
        for tarea in tareas:
            try:
                estado = "Completada" if tarea.completada else "Pendiente"
                
                # Formatear fecha de manera segura
                if hasattr(tarea.fecha_vencimiento, 'strftime'):
                    fecha = tarea.fecha_vencimiento.strftime("%d/%m/%Y")
                else:
                    fecha = str(tarea.fecha_vencimiento)
                
                valores = (tarea.prioridad.name, tarea.titulo, fecha, estado)
                item = self.tree_tareas.insert("", "end", values=valores)
                
                # Guardar ID para referencia
                self.tree_tareas.item(item, tags=(str(tarea.id),))
                
                # Asignar color según prioridad
                if tarea.prioridad == Prioridad.BAJA:
                    self.tree_tareas.tag_configure(str(tarea.id), foreground="green")
                elif tarea.prioridad == Prioridad.MEDIA:
                    self.tree_tareas.tag_configure(str(tarea.id), foreground="blue")
                elif tarea.prioridad == Prioridad.ALTA:
                    self.tree_tareas.tag_configure(str(tarea.id), foreground="orange")
                elif tarea.prioridad == Prioridad.URGENTE:
                    self.tree_tareas.tag_configure(str(tarea.id), foreground="red")
            except Exception as e:
                print(f"Error al insertar tarea '{tarea.titulo}': {e}")
    
    def _seleccionar_categoria(self, event):
        seleccion = self.tree_categorias.selection()
        if seleccion:
            self.categoria_seleccionada = seleccion[0]
            self._actualizar_tareas()
            print(f"Categoría seleccionada: {self.categoria_seleccionada}")  # Depuración
            
            # Verificar tareas en esta categoría (depuración)
            tareas = self.gestor_tareas.obtener_tareas_por_categoria(self.categoria_seleccionada)
            print(f"Encontradas {len(tareas)} tareas en esta categoría")  # Depuración
    
    def _seleccionar_tarea(self, event):
        seleccion = self.tree_tareas.selection()
        if seleccion:
            item = seleccion[0]
            tags = self.tree_tareas.item(item, "tags")
            if tags:
                tarea_id = int(tags[0])
                self.tarea_seleccionada = tarea_id
    
    def _nueva_categoria(self):
        nombre = simpledialog.askstring("Nueva Categoría", "Nombre de la categoría:")
        if nombre:
            if self.categoria_seleccionada and self.categoria_seleccionada != "todas":
                # Crear subcategoría
                ruta = f"{self.categoria_seleccionada}/{nombre}"
            else:
                ruta = nombre
                
            self.gestor_tareas.arbol_categorias.agregar_categoria(ruta)
            self._actualizar_listas()
            self._actualizar_historial()
            self.barra_estado.config(text=f"Categoría '{nombre}' creada")
    
    def _nueva_tarea(self):
        # Ventana para nueva tarea
        ventana = tk.Toplevel(self.root)
        ventana.title("Nueva Tarea")
        ventana.geometry("400x350")
        ventana.resizable(False, False)
        ventana.grab_set()  # Modal
        
        ttk.Label(ventana, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        titulo_var = tk.StringVar()
        ttk.Entry(ventana, textvariable=titulo_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(ventana, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        descripcion_text = tk.Text(ventana, width=30, height=5)
        descripcion_text.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(ventana, text="Prioridad:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        prioridad_var = tk.IntVar(value=1)
        
        frame_prioridad = ttk.Frame(ventana)
        frame_prioridad.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        for i, p in enumerate(Prioridad):
            ttk.Radiobutton(frame_prioridad, text=p.name, variable=prioridad_var, 
                          value=p.value).grid(row=0, column=i, padx=5)
        
        ttk.Label(ventana, text="Fecha Vencimiento:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        cal = tkcalendar.DateEntry(ventana, width=12, background='darkblue',
                                  foreground='white', borderwidth=2)
        cal.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(ventana, text="Categoría:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        categoria_var = tk.StringVar()
        
        categorias = [""] + [ruta for ruta, _, _ in self.gestor_tareas.obtener_todas_categorias()]
        combo_categorias = ttk.Combobox(ventana, textvariable=categoria_var, values=categorias, width=28)
        combo_categorias.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        if self.categoria_seleccionada and self.categoria_seleccionada != "todas":
            categoria_var.set(self.categoria_seleccionada)
        
        def guardar():
            titulo = titulo_var.get().strip()
            if not titulo:
                messagebox.showerror("Error", "El título es obligatorio")
                return
                
            descripcion = descripcion_text.get("1.0", tk.END).strip()
            valor_prioridad = prioridad_var.get()
            prioridad = next(p for p in Prioridad if p.value == valor_prioridad)
            
            # Convertir el objeto date a datetime para mantener consistencia
            fecha = cal.get_date()
            from datetime import datetime
            fecha_dt = datetime.combine(fecha, datetime.min.time())
            
            categoria = categoria_var.get()
            
            self.gestor_tareas.crear_tarea(titulo, descripcion, prioridad, fecha_dt, categoria)
            self._actualizar_listas()
            self._actualizar_historial()
            ventana.destroy()
            self.barra_estado.config(text=f"Tarea '{titulo}' creada")
        
        frame_botones = ttk.Frame(ventana)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Guardar", command=guardar).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy).grid(row=0, column=1, padx=5)
    
    def _editar_tarea(self):
        if not self.tarea_seleccionada:
            messagebox.showinfo("Información", "Seleccione una tarea para editar")
            return
            
        tarea = self.gestor_tareas.lista_tareas.obtener_tarea(self.tarea_seleccionada)
        if not tarea:
            messagebox.showerror("Error", "Tarea no encontrada")
            return
        
        # Ventana para editar tarea (similar a nueva tarea)
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Tarea")
        ventana.geometry("400x350")
        ventana.resizable(False, False)
        ventana.grab_set()  # Modal
        
        ttk.Label(ventana, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        titulo_var = tk.StringVar(value=tarea.titulo)
        ttk.Entry(ventana, textvariable=titulo_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(ventana, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        descripcion_text = tk.Text(ventana, width=30, height=5)
        descripcion_text.insert("1.0", tarea.descripcion)
        descripcion_text.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(ventana, text="Prioridad:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        prioridad_var = tk.IntVar(value=tarea.prioridad.value)
        
        frame_prioridad = ttk.Frame(ventana)
        frame_prioridad.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        for i, p in enumerate(Prioridad):
            ttk.Radiobutton(frame_prioridad, text=p.name, variable=prioridad_var, 
                          value=p.value).grid(row=0, column=i, padx=5)
        
        ttk.Label(ventana, text="Fecha Vencimiento:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        cal = tkcalendar.DateEntry(ventana, width=12, background='darkblue',
                                  foreground='white', borderwidth=2)
        cal.set_date(tarea.fecha_vencimiento)
        cal.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(ventana, text="Categoría:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        categoria_var = tk.StringVar(value=tarea.categoria if tarea.categoria else "")
        
        categorias = [""] + [ruta for ruta, _, _ in self.gestor_tareas.obtener_todas_categorias()]
        combo_categorias = ttk.Combobox(ventana, textvariable=categoria_var, values=categorias, width=28)
        combo_categorias.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        def guardar():
            titulo = titulo_var.get().strip()
            if not titulo:
                messagebox.showerror("Error", "El título es obligatorio")
                return
                
            descripcion = descripcion_text.get("1.0", tk.END).strip()
            valor_prioridad = prioridad_var.get()
            prioridad = next(p for p in Prioridad if p.value == valor_prioridad)
            
            # Convertir el objeto date a datetime para mantener consistencia
            fecha = cal.get_date()
            from datetime import datetime
            fecha_dt = datetime.combine(fecha, datetime.min.time())
            
            categoria = categoria_var.get()
            
            self.gestor_tareas.actualizar_tarea(
                self.tarea_seleccionada,
                titulo=titulo,
                descripcion=descripcion,
                prioridad=prioridad,
                fecha_vencimiento=fecha_dt,
                categoria=categoria
            )
            
            self._actualizar_listas()
            self._actualizar_historial()
            ventana.destroy()
            self.barra_estado.config(text=f"Tarea '{titulo}' actualizada")
        
        frame_botones = ttk.Frame(ventana)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Guardar", command=guardar).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy).grid(row=0, column=1, padx=5)
    
    def _eliminar_tarea(self):
        if not self.tarea_seleccionada:
            messagebox.showinfo("Información", "Seleccione una tarea para eliminar")
            return
            
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta tarea?")
        if confirmar:
            tarea = self.gestor_tareas.eliminar_tarea(self.tarea_seleccionada)
            if tarea:
                self._actualizar_listas()
                self._actualizar_historial()
                self.barra_estado.config(text=f"Tarea '{tarea.titulo}' eliminada")
                self.tarea_seleccionada = None
    
    def _completar_tarea(self):
        if not self.tarea_seleccionada:
            messagebox.showinfo("Información", "Seleccione una tarea para marcar como completada")
            return
            
        tarea = self.gestor_tareas.lista_tareas.obtener_tarea(self.tarea_seleccionada)
        if tarea:
            tarea.marcar_completada()
            self._actualizar_listas()
            self._actualizar_historial()
            self.barra_estado.config(text=f"Tarea '{tarea.titulo}' marcada como completada")
    
    def _actualizar_historial(self):
        """Actualiza la visualización del historial de acciones"""
        # Limpiar lista actual
        self.tree_historial.delete(*self.tree_historial.get_children())
        
        # Cargar acciones desde el historial (en orden inverso para mostrar las más recientes primero)
        for i, accion in enumerate(reversed(self.gestor_tareas.historial_acciones.pila_deshacer)):
            indice = len(self.gestor_tareas.historial_acciones.pila_deshacer) - i
            
            # Determinar tipo de acción en español
            if accion.tipo_accion == "AGREGAR":
                tipo = "Agregar"
                detalles = "Se agregó esta tarea"
            elif accion.tipo_accion == "ELIMINAR":
                tipo = "Eliminar"
                detalles = "Se eliminó esta tarea"
            elif accion.tipo_accion == "ACTUALIZAR":
                tipo = "Actualizar"
                # Crear detalles de la actualización
                cambios = []
                for key, old_value in accion.valores_antiguos.items():
                    if key == 'titulo' and old_value != accion.tarea.titulo:
                        cambios.append(f"Título: '{old_value}' → '{accion.tarea.titulo}'")
                    elif key == 'descripcion' and old_value != accion.tarea.descripcion:
                        # Truncar descripciones largas
                        old_desc = (old_value[:20] + '...') if len(old_value) > 20 else old_value
                        new_desc = (accion.tarea.descripcion[:20] + '...') if len(accion.tarea.descripcion) > 20 else accion.tarea.descripcion
                        cambios.append(f"Descripción modificada")
                    elif key == 'prioridad' and old_value != accion.tarea.prioridad:
                        cambios.append(f"Prioridad: {old_value} → {accion.tarea.prioridad}")
                    elif key == 'fecha_vencimiento' and old_value != accion.tarea.fecha_vencimiento:
                        old_date = old_value.strftime("%d/%m/%Y") if hasattr(old_value, 'strftime') else str(old_value)
                        new_date = accion.tarea.fecha_vencimiento.strftime("%d/%m/%Y") if hasattr(accion.tarea.fecha_vencimiento, 'strftime') else str(accion.tarea.fecha_vencimiento)
                        cambios.append(f"Fecha: {old_date} → {new_date}")
                    elif key == 'categoria' and old_value != accion.tarea.categoria:
                        cambios.append(f"Categoría: '{old_value or 'Sin categoría'}' → '{accion.tarea.categoria or 'Sin categoría'}'")
                
                detalles = ", ".join(cambios) if cambios else "No hay cambios significativos"
            
            self.tree_historial.insert("", "end", values=(indice, tipo, accion.tarea.titulo, detalles))
        
        # Actualizar estadísticas
        total_acciones = len(self.gestor_tareas.historial_acciones.pila_deshacer)
        total_rehacer = len(self.gestor_tareas.historial_acciones.pila_rehacer)
        
        self.lbl_total_acciones.config(text=f"Total de acciones: {total_acciones}")
        self.lbl_total_rehacer.config(text=f"Acciones para rehacer: {total_rehacer}")
    
    def _deshacer(self):
        if self.gestor_tareas.deshacer():
            self._actualizar_listas()
            self._actualizar_historial()
            self.barra_estado.config(text="Acción deshecha")
        else:
            self.barra_estado.config(text="No hay acciones para deshacer")
    
    def _rehacer(self):
        if self.gestor_tareas.rehacer():
            self._actualizar_listas()
            self._actualizar_historial()
            self.barra_estado.config(text="Acción rehecha")
        else:
            self.barra_estado.config(text="No hay acciones para rehacer")
    
    def _procesar_urgente(self):
        tarea = self.gestor_tareas.procesar_siguiente_urgente()
        if tarea:
            tarea.marcar_completada()
            self._actualizar_listas()
            self._actualizar_historial()
            self.barra_estado.config(text=f"Tarea urgente '{tarea.titulo}' procesada")
        else:
            self.barra_estado.config(text="No hay tareas urgentes pendientes")


def iniciar_interfaz_grafica(gestor=None):
    root = tk.Tk()
    if gestor:
        app = InterfazGrafica(root, gestor)
    else:
        app = InterfazGrafica(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz_grafica() 