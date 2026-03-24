import json


class Task:
    def __init__(self, task_id, description, completed=False):
        self.task_id = task_id
        self.description = description
        self.completed = completed

    def __str__(self):
        status="✓" if self.completed else " "
        return f"[{status}] #{self.task_id}: {self.description}"
    
class TaskManager:
    FILENAME = "tasks.json"

    def __init__(self):
        self._tasks = []
        self._next_id = 1
        self.load_tasks()

    def add_task(self, description):
        new_task = Task(self._next_id, description)
        self._tasks.append(new_task)
        self._next_id += 1
        print(f"Tarea añadida: {description}")
        self.save_tasks()

    def complete_task(self, task_id):
        for current_task in self._tasks:
            if current_task.task_id == task_id:
                current_task.completed = True
                print(f"Tarea completada: {current_task}")
                self.save_tasks()
                return
        return print(f"No se encontró la tarea con ID: #{task_id}")

    def delete_task(self, task_id):
        for current_task in self._tasks:
            if current_task.task_id == task_id:
                self._tasks.remove(current_task)
                print(f"Tarea eliminada: #{task_id}")   
                self.save_tasks()
                return
        print(f"No se encontró la tarea con ID: #{task_id}")

    def list_tasks(self):
        if not self._tasks:
            print("No hay tareas.")
        else:
            for current_task in self._tasks:
                print(current_task)
    
    def load_tasks(self):
        try:
            with open(self.FILENAME, "r") as file:
                data = json.load(file)
                self._tasks = [Task(item["task_id"], item["description"], item["completed"]) for item in data]
                if self._tasks:
                    self._next_id = self._tasks[-1].task_id + 1
                else:
                    self._next_id = 1

        except FileNotFoundError:
            self._tasks = []

    def save_tasks(self):
        with open(self.FILENAME, "w") as file:
            json.dump([{
                "task_id": task.task_id,
                "description": task.description,
                "completed": task.completed
            } for task in self._tasks], file,indent=4)