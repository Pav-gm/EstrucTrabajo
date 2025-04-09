import sys
from task_manager.interfaz_grafica import iniciar_interfaz_grafica
from task_manager.demo_datos import ejecutar_demo, cargar_datos_demo

def main():
    # Verificar si hay argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Ejecutar solo la demostración en consola
        ejecutar_demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "--demo-gui":
        # Iniciar la interfaz gráfica con datos de demostración precargados
        from task_manager.gestor_tareas import GestorTareas
        gestor = GestorTareas()
        gestor = cargar_datos_demo(gestor)
        iniciar_interfaz_grafica(gestor)
    else:
        # Iniciar normalmente la interfaz gráfica
        iniciar_interfaz_grafica()

if __name__ == "__main__":
    main() 