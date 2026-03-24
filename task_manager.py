class task:
    def __init__(self,id,description,completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status="✓" if self.completed else " "