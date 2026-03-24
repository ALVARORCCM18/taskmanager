class Task:
    def __init__(self,id,description,completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status="✓" if self.completed else " "
        return f"[{status}] #{self.id}: {self.description}"
    
class TaskManager:
    def __init__(self):
        self._tasks = []
        self._next_id = 1

    def add_task(self, description):
        new_task = Task(self._next_id, description)
        self._tasks.append(new_task)
        self._next_id += 1
        print(f"Tarea añadida: {description}")

    def complete_task(self, id):
        for current_task in self._tasks:
            if current_task.id == id:
                current_task.completed = True
                print(f"Tarea completada: {current_task}")
                return
        return print(f"No se encontró la tarea con ID: #{id}")

    def delete_task(self, id):
        for current_task in self._tasks:
            if current_task.id == id:
                self._tasks.remove(current_task)
                print(f"Tarea eliminada: #{id}")   
                return
        print(f"No se encontró la tarea con ID: #{id}")

    def list_tasks(self):
        if not self._tasks:
            print("No hay tareas.")
        else:
            for current_task in self._tasks:
                print(current_task)