"""
Suite de Tests Unitarios para el Gestor de Tareas
==================================================

Proporciona cobertura completa de tests para las clases Task y TaskManager.
Incluye 20 tests que validan:
- Creación y representación de tareas
- Operaciones CRUD del gestor
- Persistencia en archivo JSON
- Casos edge y comportamientos esperados

Ejecutar con:
    python -m unittest test_task_manager -v

Autor: Master Big School IA
Versión: 1.0
"""

import unittest
import json
import os
from task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    """Tests unitarios para la clase Task"""
    
    def test_task_creation(self):
        """Validar creación básica de una tarea"""
        task = Task(1, "Test task")
        # Validar que los atributos se asignen correctamente
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.description, "Test task")
        self.assertFalse(task.completed)
    
    def test_task_creation_with_completed(self):
        """Validar creación de tarea con estado completado"""
        task = Task(2, "Completed task", completed=True)
        # Validar que el estado se asigne correctamente
        self.assertTrue(task.completed)
    
    def test_task_str_incomplete(self):
        """Validar representación en string de tarea incompleta"""
        task = Task(1, "Test task")
        # Validar formato: [ ] #ID: descripción
        self.assertEqual(str(task), "[ ] #1: Test task")
    
    def test_task_str_complete(self):
        """Validar representación en string de tarea completada"""
        task = Task(1, "Test task", completed=True)
        # Validar formato: [✓] #ID: descripción
        self.assertEqual(str(task), "[✓] #1: Test task")


class TestTaskManager(unittest.TestCase):
    """Tests unitarios para la clase TaskManager"""
    
    def setUp(self):
        """
        Preparación antes de cada test.
        
        - Configura archivo de test separado para no afectar datos reales
        - Crea instancia limpia del gestor de tareas
        """
        self.test_filename = "test_tasks.json"
        # Usar archivo de test en lugar del archivo real
        TaskManager.FILENAME = self.test_filename
        self.manager = TaskManager()
    
    def tearDown(self):
        """
        Limpieza después de cada test.
        
        - Elimina el archivo temporal de test
        """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_taskmanager_initialization(self):
        """Validar inicialización del gestor"""
        # Validar estado inicial
        self.assertEqual(len(self.manager._tasks), 0)
        self.assertEqual(self.manager._next_id, 1)
    
    def test_add_task(self):
        """Validar añadir una tarea individual"""
        self.manager.add_task("Test task 1")
        # Validar que la tarea se añadió correctamente
        self.assertEqual(len(self.manager._tasks), 1)
        self.assertEqual(self.manager._tasks[0].description, "Test task 1")
        self.assertEqual(self.manager._tasks[0].task_id, 1)
    
    def test_add_multiple_tasks(self):
        """Validar que los IDs se incrementan automáticamente al añadir múltiples"""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")
        # Validar cantidad y IDs
        self.assertEqual(len(self.manager._tasks), 3)
        self.assertEqual(self.manager._tasks[0].task_id, 1)
        self.assertEqual(self.manager._tasks[1].task_id, 2)
        self.assertEqual(self.manager._tasks[2].task_id, 3)
    
    def test_complete_task_success(self):
        """Validar completar una tarea existente"""
        self.manager.add_task("Task to complete")
        self.manager.complete_task(1)
        # Validar que el estado cambió a completado
        self.assertTrue(self.manager._tasks[0].completed)
    
    def test_complete_task_nonexistent(self):
        """Validar intentar completar una tarea inexistente"""
        self.manager.add_task("Task 1")
        # Intentar completar una tarea que no existe
        self.manager.complete_task(999)
        # Validar que la tarea existente no se cambió
        self.assertFalse(self.manager._tasks[0].completed)
    
    def test_delete_task_success(self):
        """Validar eliminar una tarea existente"""
        self.manager.add_task("Task to delete")
        self.manager.delete_task(1)
        # Validar que la lista quedó vacía
        self.assertEqual(len(self.manager._tasks), 0)
    
    def test_delete_task_nonexistent(self):
        """Validar intentar eliminar una tarea inexistente"""
        self.manager.add_task("Task 1")
        initial_count = len(self.manager._tasks)
        # Intentar eliminar una tarea que no existe
        self.manager.delete_task(999)
        # Validar que la cantidad no cambió
        self.assertEqual(len(self.manager._tasks), initial_count)
    
    def test_delete_specific_task_from_multiple(self):
        """Validar eliminar una tarea específica cuando hay múltiples"""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        self.manager.add_task("Task 3")
        # Eliminar la tarea del medio
        self.manager.delete_task(2)
        # Validar que quedaron las otras dos
        self.assertEqual(len(self.manager._tasks), 2)
        self.assertEqual(self.manager._tasks[0].task_id, 1)
        self.assertEqual(self.manager._tasks[1].task_id, 3)
    
    def test_list_tasks_empty(self):
        """Validar listar tareas cuando no hay ninguna"""
        self.assertEqual(len(self.manager._tasks), 0)
    
    def test_list_tasks_with_tasks(self):
        """Validar listar múltiples tareas"""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        # Validar que la cantidad es correcta
        self.assertEqual(len(self.manager._tasks), 2)
    
    def test_save_tasks(self):
        """Validar que las tareas se guardan en archivo JSON correctamente"""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        # Validar que el archivo fue creado
        self.assertTrue(os.path.exists(self.test_filename))
        
        # Leer el archivo y validar contenido
        with open(self.test_filename, "r") as file:
            data = json.load(file)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["description"], "Task 1")
            self.assertEqual(data[1]["description"], "Task 2")
    
    def test_load_tasks_from_file(self):
        """Validar cargar tareas desde archivo guardado"""
        # Guardar algunas tareas
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        
        # Crear nuevo gestor (debe cargar del archivo)
        new_manager = TaskManager()
        # Validar que las tareas se cargaron correctamente
        self.assertEqual(len(new_manager._tasks), 2)
        self.assertEqual(new_manager._tasks[0].description, "Task 1")
        self.assertEqual(new_manager._tasks[1].description, "Task 2")
        # Validar que el next_id se restauró correctamente
        self.assertEqual(new_manager._next_id, 3)
    
    def test_load_tasks_file_not_found(self):
        """Validar comportamiento cuando el archivo no existe"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        
        # Crear gestor con archivo inexistente
        manager = TaskManager()
        # Validar inicialización correcta
        self.assertEqual(len(manager._tasks), 0)
        self.assertEqual(manager._next_id, 1)
    
    def test_persistence_across_instances(self):
        """Validar que los datos persisten entre instancias del gestor"""
        # Crear y guardar una tarea
        self.manager.add_task("Persistent task")
        self.manager.complete_task(1)
        
        # Crear nuevo gestor que carga los datos
        new_manager = TaskManager()
        # Validar que la tarea se persitió con su estado
        self.assertTrue(new_manager._tasks[0].completed)
        self.assertEqual(new_manager._tasks[0].description, "Persistent task")
    
    def test_next_id_after_delete(self):
        """Validar que el next_id continúa incrementándose después de eliminar"""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        # Eliminar la primera tarea
        self.manager.delete_task(1)
        # Añadir nueva tarea (debe tener ID 3, no 1)
        self.manager.add_task("Task 3")
        
        # Validar IDs
        self.assertEqual(len(self.manager._tasks), 2)
        self.assertEqual(self.manager._tasks[1].task_id, 3)
    
    def test_completed_task_saved_to_file(self):
        """Validar que el estado completado se persiste en el archivo"""
        # Crear y completar una tarea
        self.manager.add_task("Task to complete")
        self.manager.complete_task(1)
        
        # Crear nuevo gestor que carga los datos
        new_manager = TaskManager()
        # Validar que la tarea se cargó como completada
        self.assertTrue(new_manager._tasks[0].completed)


if __name__ == "__main__":
    # Ejecutar todos los tests
    unittest.main()
