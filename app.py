from pawpal_system import Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

# Check if 'owner' already exists in session_state
if 'owner' not in st.session_state:
    # Create and store the Owner instance if it doesn't exist
    st.session_state['owner'] = Owner(owner_id=1, name="Alex", contact_info="alex@email.com")

# Now you can safely use st.session_state['owner'] throughout your app
owner = st.session_state['owner']

# Owner name input (for demo, not used to recreate owner object)
owner_name = st.text_input("Owner name", value=st.session_state['owner'].name if 'owner' in st.session_state else "Jordan")

# --- Add Pet Form ---
st.markdown("### Add a Pet")
if 'pets' not in st.session_state:
    st.session_state['pets'] = {}

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="")
    age = st.number_input("Age", min_value=0, max_value=50, value=1)
    medical_info = st.text_input("Medical info", value="")
    submitted = st.form_submit_button("Add Pet")
    if submitted:
        # Generate a new pet_id
        pet_id = max(st.session_state['pets'].keys(), default=100, ) + 1 if st.session_state['pets'] else 101
        new_pet = Pet(
            pet_id=pet_id,
            name=pet_name,
            species=species,
            breed=breed,
            age=age,
            medical_info=medical_info,
            owner_id=st.session_state['owner'].owner_id
        )
        st.session_state['pets'][pet_id] = new_pet
        st.session_state['owner'].add_pet(pet_id)
        st.success(f"Added pet: {pet_name}")

# Display pets
if st.session_state['owner'].pet_ids:
    st.markdown("### Your Pets")
    pet_table = []
    for pid in st.session_state['owner'].pet_ids:
        pet = st.session_state['pets'].get(pid)
        if pet:
            pet_table.append({
                "Name": pet.name,
                "Species": pet.species,
                "Breed": pet.breed,
                "Age": pet.age,
                "Medical Info": pet.medical_info
            })
    st.table(pet_table)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """

Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )