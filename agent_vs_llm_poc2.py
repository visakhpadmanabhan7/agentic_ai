import os
from datetime import datetime
from langchain_ollama import OllamaLLM
from crewai import Agent, Task, Crew

# Prompt shared by both methods
MEAL_PROMPT = (
    "Create a detailed 7-day plant-based meal plan for someone looking to gain muscle.\n"
    "Include breakfast, lunch, dinner, and one snack per day.\n"
    "Ensure each day provides 120–150g of protein."
)


def generate_filename(method_name: str, user_name: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_user = user_name.strip().lower().replace(" ", "_")
    folder = os.path.join("outputs", safe_user)
    os.makedirs(folder, exist_ok=True)  # ✅ Create folder if needed
    return os.path.join(folder, f"{method_name}_{safe_user}_{timestamp}.txt")


def generate_with_raw_llm_streamed(user_name: str):
    llm = OllamaLLM(model="mistral", streaming=True)
    filename = generate_filename("raw_llm", user_name)

    print("\n🧠 [Raw LLM] Streaming response...\n")
    with open(filename, "w") as f:
        f.write("Method: Raw LLM (Mistral)\n")
        f.write("=" * 60 + "\n\n")
        for chunk in llm.stream(MEAL_PROMPT):
            print(chunk, end="", flush=True)
            f.write(chunk)

    print(f"\n✅ Output saved to: {filename}")


def generate_with_agent_and_log(user_name: str):
    llm = OllamaLLM(model="ollama/mistral")
    filename = generate_filename("agent_crewai", user_name)

    nutritionist = Agent(
        role="Nutritionist",
        goal="Create a 7-day plant-based high-protein meal plan",
        backstory="A certified sports nutritionist specialized in vegan muscle-building diets.",
        verbose=True,
        llm=llm
    )

    meal_task = Task(
        description=MEAL_PROMPT,
        expected_output="A 7-day plant-based meal plan with 4 meals per day and daily protein targets.",
        agent=nutritionist
    )

    crew = Crew(
        agents=[nutritionist],
        tasks=[meal_task],
        verbose=True
    )

    print("\n🤖 [CrewAI] Running agent...\n")
    result = crew.kickoff()

    with open(filename, "w") as f:
        f.write("Method: Agent-based (CrewAI)\n")
        f.write("=" * 60 + "\n\n")
        f.write(str(result))
    print(f"\n✅ Output saved to: {filename}")


def main():
    print("\n👋 Welcome to FitAgent Comparison Tool!")
    user_name = input("Enter your name: ").strip()

    print("\n🔍 Choose mode:")
    print("1. Agent-based (CrewAI)")
    print("2. Raw LLM (streamed)")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        generate_with_agent_and_log(user_name)
    elif choice == "2":
        generate_with_raw_llm_streamed(user_name)
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()