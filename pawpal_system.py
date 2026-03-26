# Logic layer for PawPal system

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timedelta



@dataclass
class Task:
    task_id: int
    description: str
    time: str  # "HH:MM"
    frequency: str  # "Daily", "Weekly", etc.
    date: str = None  # "YYYY-MM-DD" (optional, for recurring logic)
    status: str = "incomplete"
    assigned_pet_id: Optional[int] = None

    def mark_complete(self, tasks_registry=None, auto_recur=True):
        """Mark the task as complete. If recurring, auto-create next occurrence."""
        self.status = "complete"
        if auto_recur and self.frequency.lower() in ("daily", "weekly") and tasks_registry is not None:
            # Parse current date
            if self.date:
                current_date = datetime.strptime(self.date, "%Y-%m-%d")
            else:
                current_date = datetime.today()
            # Calculate next date
            if self.frequency.lower() == "daily":
                next_date = current_date + timedelta(days=1)
            elif self.frequency.lower() == "weekly":
                next_date = current_date + timedelta(weeks=1)
            else:
                return
            # Create new task instance for next occurrence
            new_task_id = max(tasks_registry.keys(), default=0) + 1
            new_task = Task(
                task_id=new_task_id,
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                date=next_date.strftime("%Y-%m-%d"),
                assigned_pet_id=self.assigned_pet_id
            )
            tasks_registry[new_task_id] = new_task

    def edit_task(self, **kwargs):
        """Edit task attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete_task(self):
        """Delete the task (mark as deleted)."""
        self.status = "deleted"


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
        """Add a task to the pet."""
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)

    def edit_task(self, task_id: int, tasks: Dict[int, Task], **kwargs):
        """Edit a task for the pet."""
        if task_id in self.task_ids and task_id in tasks:
            tasks[task_id].edit_task(**kwargs)

    def delete_task(self, task_id: int):
        """Delete a task from the pet."""
        if task_id in self.task_ids:
            self.task_ids.remove(task_id)

    def get_tasks(self, tasks: Dict[int, Task]):
        """Get all tasks for the pet."""
        return [tasks[tid] for tid in self.task_ids if tid in tasks]

    def update_info(self, **kwargs):
        """Update pet information."""
        for key, value in kwargs.items():
            setattr(self, key, value)

class Owner:
    def __init__(self, owner_id: int, name: str, contact_info: str):
        self.owner_id = owner_id
        self.name = name
        self.contact_info = contact_info
        self.pet_ids: List[int] = []  # List of pet IDs only

    def add_pet(self, pet_id: int):
        """Add a pet to the owner."""
        if pet_id not in self.pet_ids:
            self.pet_ids.append(pet_id)

    def remove_pet(self, pet_id: int):
        """Remove a pet from the owner."""
        if pet_id in self.pet_ids:
            self.pet_ids.remove(pet_id)

    def get_pets(self, pets: Dict[int, Pet]):
        """Get all pets for the owner."""
        return [pets[pid] for pid in self.pet_ids if pid in pets]

    def get_all_tasks(self, pets: Dict[int, Pet], tasks: Dict[int, Task]):
        """Get all tasks for all pets owned by the owner."""
        all_tasks = []
        for pet in self.get_pets(pets):
            all_tasks.extend(pet.get_tasks(tasks))
        return all_tasks

    def update_info(self, **kwargs):
        """Update owner information."""
        for key, value in kwargs.items():
            setattr(self, key, value)


class Scheduler:
    def detect_conflicts(self):
        """
        Detect tasks scheduled at the same time for the same or different pets.
        Returns:
            List[str]: List of warning messages for detected conflicts.
        Notes:
            Only exact time and date matches are considered as conflicts.
        """
        warnings = []
        seen = {}
        for task in self.tasks:
            # Use (date, time) as key, include pet for more detail
            key = (getattr(task, 'date', None), task.time)
            if key in seen:
                other = seen[key]
                msg = (
                    f"Warning: Task '{task.description}' (Pet ID: {task.assigned_pet_id}) "
                    f"conflicts with '{other.description}' (Pet ID: {other.assigned_pet_id}) at {task.time} "
                    f"on {getattr(task, 'date', 'N/A')}."
                )
                warnings.append(msg)
            else:
                seen[key] = task
        return warnings
    def filter_by_status(self, status: str):
        """
        Filter tasks by their completion status.
        Args:
            status (str): The status to filter by (e.g., 'complete', 'incomplete').
        Returns:
            List[Task]: List of Task objects matching the given status.
        """
        return [task for task in self.tasks if getattr(task, 'status', None) == status]

    def filter_by_pet_name(self, pets: dict, pet_name: str):
        """
        Filter tasks assigned to a pet with the given name.
        Args:
            pets (dict): Dictionary of pet_id to Pet objects.
            pet_name (str): The name of the pet to filter by.
        Returns:
            List[Task]: List of Task objects assigned to the specified pet name.
        """
        pet_ids = [pid for pid, pet in pets.items() if getattr(pet, 'name', None) == pet_name]
        return [task for task in self.tasks if getattr(task, 'assigned_pet_id', None) in pet_ids]
    def sort_by_time(self):
        """
        Sort tasks by their time attribute (HH:MM format).
        Returns:
            List[Task]: List of Task objects sorted by time.
        """
        self.tasks = sorted(self.tasks, key=lambda t: tuple(map(int, t.time.split(":"))))
        return self.tasks
    def __init__(self, tasks: List[Task], constraints=None):
        self.tasks = tasks
        self.constraints = constraints
        self.plan = None

    def generate_plan(self):
        """Generate a plan for tasks."""
        self.plan = sorted(self.tasks.values(), key=lambda t: t.time)
        return self.plan

    def explain_reasoning(self):
        """Explain the reasoning behind the plan."""
        return "Tasks are scheduled based on their time attribute."

    def update_constraints(self, constraints):
        """Update scheduling constraints."""
        self.constraints = constraints

    def get_plan(self):
        """Get the current plan."""
        return self.plan

    def get_owner_tasks(self, owner: Owner, pets: Dict[int, Pet]):
        """Retrieve all tasks for all pets owned by the owner."""
        return owner.get_all_tasks(pets, self.tasks)
