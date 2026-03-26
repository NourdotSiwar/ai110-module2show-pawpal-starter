# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Scheduling

PawPal+ now includes several smarter scheduling features:

- **Sorting and Filtering:** Tasks can be sorted by time and filtered by completion status or by pet name, making it easy to view and manage daily routines.
- **Recurring Task Automation:** When a daily or weekly task is marked complete, a new instance is automatically created for the next occurrence using accurate date calculations with Python's `timedelta`.
- **Conflict Detection:** The scheduler detects and warns if two tasks (for the same or different pets) are scheduled at the same time, helping avoid accidental overlaps.

These features make the app more efficient and user-friendly for busy pet owners, ensuring that care routines are consistent, conflicts are avoided, and recurring needs are never missed.

### Testing PawPal_+
The current 7-test suite checks core logic paths including task completion state changes, pet task assignment, chronological sorting, daily recurrence creation on completion, duplicate time conflict detection, empty-scheduler behavior, and non-conflict handling for same times on different dates.

Command to run tests: python -m pytest

Confidence Level for system readability (based on 7/7 passing tests): ★★★★☆ (4/5)

Reason:

- Passing tests give strong confidence that key behaviors are clear and consistently implemented.
- The tests cover major happy paths and important edge cases.
- Readability is high, but not a full 5/5 because it is always possible to test more. As mentioned by Dijkstra, tests only prove presence of bugs, not their absence.
