"""
Módulo de Gestión de Tareas
============================

Define las clases Task y TaskManager para gestionar tareas.
Proporciona funcionalidad de persistencia en JSON y operaciones CRUD completas.

Autor: Master Big School IA
Versión: 1.0
"""

import json


class Task:
    """
    Clase que representa una tarea individual.
    
    Atributos:
        task_id (int): Identificador único de la tarea
        description (str): Descripción o título de la tarea
        completed (bool): Estado de completación de la tarea. Por defecto False
    
    Ejemplo:
        >>> task = Task(1, "Comprar leche")
        >>> task.task_id
        1
        >>> str(task)
        '[ ] #1: Comprar leche'
    """
    
    def __init__(self, task_id, description, completed=False):
        """
        Inicializa una nueva tarea.
        
        Args:
            task_id (int): Identificador único de la tarea
            description (str): Descripción de la tarea
            completed (bool): Estado inicial de completación. Por defecto False
        """
        self.task_id = task_id
        self.description = description
        self.completed = completed

    def __str__(self):
        """
        Retorna una representación en string de la tarea.
        
        Formato: [✓/espacio] #ID: descripción
        - Usa ✓ si está completada
        - Usa espacio en blanco si no está completada
        
        Returns:
            str: Representación formateada de la tarea
        """
        # Determinar símbolo según estado de completación
        status = "✓" if self.completed else " "
        # Retornar formato [status] #ID: descripción
        return f"[{status}] #{self.task_id}: {self.description}"

    
class TaskManager:
    """
    Gestor de tareas con persistencia en JSON.
    
    Proporciona funcionalidades:
    - Crear (add_task)
    - Leer (list_tasks)
    - Actualizar (complete_task)
    - Eliminar (delete_task)
    - Persistir datos (save_tasks, load_tasks)
    
    Las tareas se guardan automáticamente en tasks.json después de cada cambio.
    
    Atributos de clase:
        FILENAME (str): Nombre del archivo JSON de persistencia
    
    Atributos de instancia:
        _tasks (list): Lista de objetos Task
        _next_id (int): Próximo ID a asignar (auto-incrementa)
    
    Ejemplo:
        >>> manager = TaskManager()
        >>> manager.add_task("Mi primera tarea")
        Tarea añadida: Mi primera tarea
        >>> manager.list_tasks()
        [ ] #1: Mi primera tarea
    """
    
    # Nombre del archivo donde se persisten las tareas
    FILENAME = "tasks.json"

    def __init__(self):
        """
        Inicializa el gestor de tareas.
        
        - Crea una lista vacía de tareas
        - Inicializa el contador de IDs en 1
        - Carga tareas desde el archivo JSON (si existe)
        """
        self._tasks = []
        self._next_id = 1
        # Cargar tareas previas si existen
        self.load_tasks()

    def add_task(self, description):
        """
        Añade una nueva tarea al gestor.
        
        - Crea una tarea con el próximo ID disponible
        - La añade a la lista de tareas
        - Incrementa el contador de IDs
        - Guarda automáticamente los cambios
        
        Args:
            description (str): Descripción de la tarea a añadir
        """
        # Crear nueva tarea con próximo ID disponible
        new_task = Task(self._next_id, description)
        # Añadir a la lista de tareas
        self._tasks.append(new_task)
        # Incrementar para la próxima tarea
        self._next_id += 1
        # Mostrar confirmación
        print(f"Tarea añadida: {description}")
        # Persistir cambios en archivo
        self.save_tasks()

    def complete_task(self, task_id):
        """
        Marca una tarea como completada.
        
        Busca la tarea con el ID proporcionado y:
        - Cambia su estado a completado (True)
        - Muestra la tarea actualizada
        - Guarda automáticamente los cambios
        - Si no encuentra la tarea, muestra un mensaje de error
        
        Args:
            task_id (int): ID de la tarea a completar
        """
        # Buscar tarea con el ID proporcionado
        for current_task in self._tasks:
            if current_task.task_id == task_id:
                # Marcar como completada
                current_task.completed = True
                # Mostrar resultado
                print(f"Tarea completada: {current_task}")
                # Persistir cambios
                self.save_tasks()
                # Salir después de encontrar y actualizar
                return
        # Si no encuentra la tarea, mostrar error
        return print(f"No se encontró la tarea con ID: #{task_id}")

    def delete_task(self, task_id):
        """
        Elimina una tarea del gestor.
        
        Busca la tarea con el ID proporcionado y:
        - La elimina de la lista
        - Muestra confirmación de eliminación
        - Guarda automáticamente los cambios
        - Si no encuentra la tarea, muestra un mensaje de error
        
        Args:
            task_id (int): ID de la tarea a eliminar
        """
        # Buscar tarea con el ID proporcionado
        for current_task in self._tasks:
            if current_task.task_id == task_id:
                # Eliminar tarea de la lista
                self._tasks.remove(current_task)
                # Mostrar confirmación
                print(f"Tarea eliminada: #{task_id}")   
                # Persistir cambios
                self.save_tasks()
                # Salir después de eliminar
                return
        # Si no encuentra la tarea, mostrar error
        print(f"No se encontró la tarea con ID: #{task_id}")

    def list_tasks(self):
        """
        Muestra todas las tareas al usuario.
        
        Si no hay tareas, muestra "No hay tareas."
        Si hay tareas, las lista una por una con formato:
        [estado] #ID: descripción
        """
        # Validar si hay tareas
        if not self._tasks:
            print("No hay tareas.")
        else:
            # Iterar y mostrar cada tarea con su representación en string
            for current_task in self._tasks:
                print(current_task)
    
    def load_tasks(self):
        """
        Carga las tareas desde el archivo JSON.
        
        - Lee el archivo tasks.json
        - Reconstruye objetos Task a partir de los datos JSON
        - Restaura el contador de IDs al máximo ID + 1
        - Si el archivo no existe, inicializa con lista vacía
        
        Formato esperado en JSON:
        [
            {
                "task_id": 1,
                "description": "Tarea 1",
                "completed": false
            },
            ...
        ]
        """
        try:
            # Intentar abrir y leer el archivo JSON
            with open(self.FILENAME, "r") as file:
                # Parsear JSON a lista de diccionarios
                data = json.load(file)
                # Reconstruir objetos Task desde los datos
                self._tasks = [Task(item["task_id"], item["description"], item["completed"]) for item in data]
                # Restaurar el contador de IDs
                if self._tasks:
                    # Si hay tareas, el próximo ID es el máximo + 1
                    self._next_id = self._tasks[-1].task_id + 1
                else:
                    # Si no hay tareas, empezar desde 1
                    self._next_id = 1

        # Si el archivo no existe, es la primera ejecución
        except FileNotFoundError:
            self._tasks = []

    def save_tasks(self):
        """
        Guarda todas las tareas en el archivo JSON.
        
        - Convierte cada objeto Task a diccionario
        - Serializa a formato JSON
        - Escribe en tasks.json con formato indentado para legibilidad
        
        Formato guardado:
        [
            {
                "task_id": 1,
                "description": "Tarea 1",
                "completed": false
            },
            ...
        ]
        """
        # Abrir archivo en modo escritura
        with open(self.FILENAME, "w") as file:
            # Convertir tareas a diccionarios y guardar como JSON
            json.dump([{
                "task_id": task.task_id,
                "description": task.description,
                "completed": task.completed
            } for task in self._tasks], file, indent=4)