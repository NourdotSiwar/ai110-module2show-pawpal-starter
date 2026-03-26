# PawPal+ Project Reflection

## 1. System Design

- User actions:
1. Edit/Add tasks
2. See daily generated plan
3. User enters pet + owner information

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?


Initial Design:
*Owner Class*
Attributes: owner_id, name, contact_info, pets (Pet List)
Methods: add_pet(), remove_pet(), get_pets(), update_info()

*Pet Class*
Attributes: pet_id, name, species, breed, age, medical_info, owner (Owner), tasks (list of Task)
Methods: add_task(), remove_task(), get_tasks(), update_info()

*Task Class*
Attributes: task_id, description, category, due_date, status, assigned_pet (Pet)
Methods: mark_complete(), edit_task(), delete_task()

*TaskManager  Class*
Attributes: tasks (list of Task)
Methods: add_task(), edit_task(), delete_task(), get_tasks(), assign_task_to_pet()

*DailyPlanGenerator Class*
Attributes: tasks (list of Task), constraints (e.g., pet schedule, owner availability), plan
Methods: generate_plan(), explain_reasoning(), update_constraints(), get_plan()

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

CoPilot mentioned that there is a circular reference of Owner -> Pet -> Owner. So, I wanted to remove a cause for a potential infinite loop. Thus, I decided to use IDs so that Pet and Task use only IDs for references, and remove the direct object references, which would make serialization and data management easier.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- The scheduler primarily considers the time each task is scheduled for, ensuring tasks are ordered and checked for conflicts based on their time and date.
- Time was chosen as the most important constraint because, for pet care, making sure tasks do not overlap and are performed at the correct times is critical for the pets' well-being and the owner's routine. Other constraints like priority or preferences could be added in the future.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- One tradeoff the scheduler makes is that it only checks for exact time matches (tasks scheduled at the same hour and minute) when detecting conflicts, rather than considering overlapping durations or tasks that might partially overlap.
- This tradeoff is reasonable because most pet care tasks in this context are short and occur at specific times (like feeding or walking), so exact time conflicts are the most likely and relevant issue. This approach keeps the conflict detection logic simple and efficient, which is appropriate for a lightweight scheduling app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
