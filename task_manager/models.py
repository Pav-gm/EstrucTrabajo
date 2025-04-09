from datetime import datetime
from enum import Enum

class Prioridad(Enum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3
    URGENTE = 4
    
    def __str__(self):
        return self.name

class Tarea:
    def __init__(self, titulo, descripcion, prioridad, fecha_vencimiento, categoria=None):
        self.id = id(self)  # Usar id del objeto como identificador único
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fecha_vencimiento = fecha_vencimiento
        self.categoria = categoria
        self.completada = False
        
    def __str__(self):
        estado = "Completada" if self.completada else "Pendiente"
        return f"[{self.prioridad}] {self.titulo} - Vence: {self.fecha_vencimiento.strftime('%d/%m/%Y')} - {estado}"
    
    def marcar_completada(self):
        self.completada = True
        
    def marcar_pendiente(self):
        self.completada = False
        
    def actualizar(self, titulo=None, descripcion=None, prioridad=None, fecha_vencimiento=None, categoria=None):
        if titulo is not None:
            self.titulo = titulo
        if descripcion is not None:
            self.descripcion = descripcion
        if prioridad is not None:
            self.prioridad = prioridad
        if fecha_vencimiento is not None:
            self.fecha_vencimiento = fecha_vencimiento
        if categoria is not None:
            self.categoria = categoria 