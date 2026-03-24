"""
Módulo principal del Gestor de Tareas Inteligente
================================================

Este módulo proporciona la interfaz de línea de comandos para el gestor de tareas.
Utiliza un menú interactivo para permitir al usuario realizar operaciones CRUD
en tareas, incluyendo la capacidad de desglosar tareas complejas usando IA.

Autor: Master Big School IA
Versión: 1.0
"""

from task_manager import TaskManager
from ai_service import create_simple_task


def print_menu():
    """
    Muestra el menú principal del gestor de tareas.
    
    Presenta 6 opciones:
    1. Añadir tarea simple
    2. Añadir tarea compleja (con IA)
    3. Ver todas las tareas
    4. Completar una tarea
    5. Eliminar una tarea
    6. Salir del programa
    """
    print("\n-----------Gestor de tareas inteligente-----------")
    print("1. Añadir tarea")
    print("2. Añadir tarea compleja (con IA)")
    print("3. Ver tareas")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Salir")   


def main():
    """
    Función principal del programa.
    
    Ejecuta un bucle interactivo que:
    - Muestra el menú de opciones
    - Captura la entrada del usuario
    - Ejecuta la acción correspondiente
    - Maneja errores de entrada
    - Persiste los datos automáticamente
    
    El bucle continúa hasta que el usuario selecciones salir (opción 6).
    """
    # Inicializar el gestor de tareas (carga datos de tasks.json)
    task_manager = TaskManager()
    
    # Bucle principal interactivo
    while True:
        # Mostrar el menú
        print_menu()

        try:
            # Obtener la opción del usuario
            choice = int(input("Selecciona una opción: "))

            # Procesar la opción seleccionada usando match/case (Python 3.10+)
            match choice:
                # OPCIÓN 1: Añadir tarea simple
                case 1: 
                    description = input("Descripción de la tarea: ")
                    task_manager.add_task(description)
                
                # OPCIÓN 2: Añadir tarea compleja desglosada por IA
                case 2:
                    description = input("Descripción de la tarea compleja: ")
                    # Obtener subtareas generadas por OpenAI
                    subtasks = create_simple_task(description)
                    # Añadir cada subtarea generada al gestor
                    for subtask in subtasks:
                        # Validar que no sea un mensaje de error
                        if not subtask.startswith("Error:"):
                            task_manager.add_task(subtask)
                        else:
                            # Mostrar el error y salir del bucle
                            print(subtask)
                            break
                
                # OPCIÓN 3: Listar todas las tareas
                case 3:
                    task_manager.list_tasks()  
                
                # OPCIÓN 4: Completar una tarea específica
                case 4:
                    task_id = int(input("ID de la tarea a completar: ")) 
                    task_manager.complete_task(task_id)
                
                # OPCIÓN 5: Eliminar una tarea específica
                case 5:            
                    task_id = int(input("ID de la tarea a eliminar: "))
                    task_manager.delete_task(task_id)
                
                # OPCIÓN 6: Salir del programa
                case 6:
                    print("Saliendo del gestor de tareas. ¡Hasta luego!")
                    break
                
                # Opción por defecto: entrada inválida
                case _:
                    print("Opción no válida. Por favor, selecciona una opción del 1 al 6.")

        # Capturar errores de conversión a entero
        except ValueError:
            print("Entrada no válida. Por favor, ingresa otra opcion.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
