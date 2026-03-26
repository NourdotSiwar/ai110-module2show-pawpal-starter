from pawpal_system import Task, Pet, Owner, Scheduler

# Global registries for testing
pets = {}
tasks = {}

# Create an Owner
owner = Owner(owner_id=1, name="Alex", contact_info="alex@email.com")

# Create two Pets
pet1 = Pet(pet_id=101, name="Buddy", species="Dog", breed="Labrador", age=5, medical_info="Healthy", owner_id=owner.owner_id)
pet2 = Pet(pet_id=102, name="Mittens", species="Cat", breed="Siamese", age=3, medical_info="Allergic to fish", owner_id=owner.owner_id)

# Register pets
tpets = {pet1.pet_id: pet1, pet2.pet_id: pet2}
for pet in tpets.values():
    pets[pet.pet_id] = pet
    owner.add_pet(pet.pet_id)


# Create tasks out of order
task1 = Task(task_id=201, description="Morning Walk", time="08:00", frequency="Daily", assigned_pet_id=pet1.pet_id)
task2 = Task(task_id=202, description="Feed Breakfast", time="09:00", frequency="Daily", assigned_pet_id=pet2.pet_id)
task3 = Task(task_id=203, description="Vet Appointment", time="15:00", frequency="Once", assigned_pet_id=pet1.pet_id)
task4 = Task(task_id=204, description="Evening Play", time="19:00", frequency="Daily", assigned_pet_id=pet2.pet_id)
task5 = Task(task_id=205, description="Lunch Snack", time="12:30", frequency="Daily", assigned_pet_id=pet1.pet_id)

# Add out of order: 3, 1, 5, 2, 4
for t in [task3, task1, task5, task2, task4]:
    tasks[t.task_id] = t
    if t.assigned_pet_id in pets:
        pets[t.assigned_pet_id].add_task(t.task_id)


# Mark some tasks as complete and demonstrate recurring automation
print("\n--- Marking a Daily Task Complete (Feed Breakfast) ---")
task2.mark_complete(tasks_registry=tasks)
for tid, t in tasks.items():
    if t.description == "Feed Breakfast":
        print(f"Task ID: {t.task_id}, Date: {getattr(t, 'date', 'N/A')}, Status: {t.status}")

print("\n--- Marking a Daily Task Complete (Evening Play) ---")
task4.mark_complete(tasks_registry=tasks)
for tid, t in tasks.items():
    if t.description == "Evening Play":
        print(f"Task ID: {t.task_id}, Date: {getattr(t, 'date', 'N/A')}, Status: {t.status}")


# Add two tasks at the same time for conflict detection
conflict_task1 = Task(task_id=300, description="Overlap Task 1", time="10:00", frequency="Once", assigned_pet_id=pet1.pet_id, date="2026-03-26")
conflict_task2 = Task(task_id=301, description="Overlap Task 2", time="10:00", frequency="Once", assigned_pet_id=pet2.pet_id, date="2026-03-26")
tasks[conflict_task1.task_id] = conflict_task1
tasks[conflict_task2.task_id] = conflict_task2
for t in [conflict_task1, conflict_task2]:
    if t.assigned_pet_id in pets:
        pets[t.assigned_pet_id].add_task(t.task_id)

# Create Scheduler with a list of Task objects
sched_tasks = list(tasks.values())
scheduler = Scheduler(sched_tasks)


# Test conflict detection
print("\n--- Conflict Detection ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts detected.")

# Test sorting
print("\n--- Sorted by Time ---")
sorted_tasks = scheduler.sort_by_time()
for task in sorted_tasks:
    pet_name = pets[task.assigned_pet_id].name if task.assigned_pet_id in pets else "Unknown Pet"
    print(f"{task.time} - {task.description} for {pet_name} (Status: {task.status})")

# Test filtering by status
print("\n--- Completed Tasks ---")
completed = scheduler.filter_by_status("complete")
for task in completed:
    pet_name = pets[task.assigned_pet_id].name if task.assigned_pet_id in pets else "Unknown Pet"
    print(f"{task.time} - {task.description} for {pet_name} (Status: {task.status})")

# Test filtering by pet name
print("\n--- Tasks for Mittens ---")
mittens_tasks = scheduler.filter_by_pet_name(pets, "Mittens")
for task in mittens_tasks:
    pet_name = pets[task.assigned_pet_id].name if task.assigned_pet_id in pets else "Unknown Pet"
    print(f"{task.time} - {task.description} for {pet_name} (Status: {task.status})")
