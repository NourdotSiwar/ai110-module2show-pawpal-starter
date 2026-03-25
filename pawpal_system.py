# Logic layer for PawPal system
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    task_id: int
    description: str
    category: str
    due_date: str
    status: str
    assigned_pet_id: Optional[int] = None  # Reference by pet_id only

    def mark_complete(self):
        pass

    def edit_task(self, **kwargs):
        pass

    def delete_task(self):
        pass


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    breed: str
    age: int
    medical_info: str
    owner_id: Optional[int] = None  # Reference by owner_id only
    task_ids: List[int] = field(default_factory=list)  # List of task IDs only

    def add_task(self, task_id: int):
        pass

    def edit_task(self, task_id: int, **kwargs):
        pass

    def delete_task(self, task_id: int):
        pass

    def get_tasks(self):
        pass

    def update_info(self, **kwargs):
        pass

class Owner:
    def __init__(self, owner_id: int, name: str, contact_info: str):
        self.owner_id = owner_id
        self.name = name
        self.contact_info = contact_info
        self.pet_ids: List[int] = []  # List of pet IDs only

    def add_pet(self, pet_id: int):
        pass

    def remove_pet(self, pet_id: int):
        pass

    def get_pets(self):
        pass

    def update_info(self, **kwargs):
        pass



class Scheduler:
    def __init__(self, tasks: List[Task], constraints=None):
        self.tasks = tasks
        self.constraints = constraints
        self.plan = None

    def generate_plan(self):
        pass

    def explain_reasoning(self):
        pass

    def update_constraints(self, constraints):
        pass

    def get_plan(self):
        pass
