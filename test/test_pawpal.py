import pytest
from pawpal_system import Task, Pet, Scheduler

def test_task_completion():
    task = Task(task_id=1, description="Feed", time="08:00", frequency="Daily")
    assert task.status == "incomplete"
    task.mark_complete()
    assert task.status == "complete"

def test_pet_add_task():
    pet = Pet(pet_id=1, name="Buddy", species="Dog", breed="Lab", age=3, medical_info="None")
    initial_count = len(pet.task_ids)
    pet.add_task(101)
    assert len(pet.task_ids) == initial_count + 1
    assert 101 in pet.task_ids


def test_scheduler_sorting_returns_chronological_order():
    tasks = [
        Task(task_id=1, description="Walk", time="13:30", frequency="Daily"),
        Task(task_id=2, description="Feed", time="08:15", frequency="Daily"),
        Task(task_id=3, description="Play", time="10:00", frequency="Daily"),
    ]
    scheduler = Scheduler(tasks)

    sorted_tasks = scheduler.sort_by_time()

    assert [task.task_id for task in sorted_tasks] == [2, 3, 1]


def test_daily_task_completion_creates_next_day_occurrence():
    task = Task(
        task_id=1,
        description="Give medicine",
        time="09:00",
        frequency="Daily",
        date="2026-03-26",
        assigned_pet_id=10,
    )
    tasks_registry = {1: task}

    task.mark_complete(tasks_registry=tasks_registry)

    assert task.status == "complete"
    assert len(tasks_registry) == 2
    assert 2 in tasks_registry
    assert tasks_registry[2].date == "2026-03-27"
    assert tasks_registry[2].status == "incomplete"
    assert tasks_registry[2].assigned_pet_id == 10


def test_conflict_detection_flags_duplicate_date_and_time():
    tasks = [
        Task(task_id=1, description="Breakfast", time="08:00", frequency="Daily", date="2026-03-26", assigned_pet_id=1),
        Task(task_id=2, description="Walk", time="08:00", frequency="Daily", date="2026-03-26", assigned_pet_id=2),
    ]
    scheduler = Scheduler(tasks)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Breakfast" in warnings[0]
    assert "Walk" in warnings[0]


def test_scheduler_with_no_tasks_returns_empty_outputs():
    scheduler = Scheduler([])

    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.filter_by_status("incomplete") == []


def test_same_time_different_dates_are_not_conflicts():
    tasks = [
        Task(task_id=1, description="Feed", time="08:00", frequency="Daily", date="2026-03-26", assigned_pet_id=1),
        Task(task_id=2, description="Feed", time="08:00", frequency="Daily", date="2026-03-27", assigned_pet_id=1),
    ]
    scheduler = Scheduler(tasks)

    warnings = scheduler.detect_conflicts()

    assert warnings == []
