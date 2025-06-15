from crewai import Agent, Task, Crew
from langchain_ollama import OllamaLLM

# Initialize Mistral model via Ollama
llm = OllamaLLM(model="ollama/mistral")
# === Agents ===

nutritionist = Agent(
    role="Nutritionist",
    goal="Create a 7-day plant-based high-protein meal plan",
    backstory="A certified sports nutritionist specialized in vegan muscle-building diets.",
    verbose=True,
    llm=llm
)

trainer = Agent(
    role="Personal Trainer",
    goal="Design a 7-day hypertrophy workout program",
    backstory="An experienced coach helping people gain muscle efficiently and safely.",
    verbose=True,
    llm=llm
)

planner = Agent(
    role="Routine Planner",
    goal="Integrate meal and workout plans into a user-friendly weekly schedule",
    backstory="Helps users balance training and nutrition for sustainable results.",
    verbose=True,
    llm=llm
)

# === Tasks ===

meal_task = Task(
    description=(
        "Create a detailed 7-day meal plan for a plant-based user aiming to gain muscle. "
        "Include breakfast, lunch, dinner, and one snack per day. "
        "Each day should provide 120–150g of protein."
    ),
    expected_output="A day-by-day plant-based meal plan with 4 meals per day and daily protein targets.",
    agent=nutritionist
)

workout_task = Task(
    description=(
        "Build a weekly hypertrophy training plan with 5 training days and 2 rest days. "
        "Mention targeted muscle groups, key exercises, and rep schemes."
    ),
    expected_output="A 7-day workout schedule with exercise focus for each day and recovery guidance.",
    agent=trainer
)

planning_task = Task(
    description=(
        "Merge the meal and workout plans into a clear daily routine. "
        "Align meals with workouts to optimize performance and recovery."
    ),
    expected_output="A final weekly calendar showing what to eat and when to train each day.",
    agent=planner
)

# === Crew Execution ===

crew = Crew(
    agents=[nutritionist, trainer, planner],
    tasks=[meal_task, workout_task, planning_task],
    verbose=True
)

# Run the agents
result = crew.kickoff()

# Output the final result
print("\n🏁 FINAL WEEKLY PLAN:\n")
print(result)