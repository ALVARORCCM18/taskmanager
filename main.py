from task_manager import TaskManager

def print_menu():
    print("\n-----------Gestor de tareas inteligente-----------")
    print("1. Añadir tarea")
    print("2. Ver tareas")
    print("3. Completar tarea")
    print("4. Eliminar tarea")
    print("5. Salir")   

def main():

    task_manager = TaskManager()
    while True:
    
        print_menu()

        try:
            choice  = int(input("Selecciona una opción: "))

        match choice:
            case "1": 
                description = input("Descripción de la tarea: ")
                task_manager.add_task(description)
                
            case "2":
                task_manager.list_tasks()  
                
            case "3":
                id = int(input("ID de la tarea a completar: ")) 
                task_manager.complete_task(id)
                
            case "4":            
                id = int(input("ID de la tarea a eliminar: "))
                task_manager.delete_task(id)
                
            case "5":
                print("Saliendo del gestor de tareas. ¡Hasta luego!")
                break
                 
            case _:
                print("Opción no válida. Por favor, selecciona una opción del 1 al 5.")

if __name__ == "__main__":
    main()
