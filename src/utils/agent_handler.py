from crewai import Agent, Task, Crew
from langchain_ollama import OllamaLLM
from src.utils.calorie_tool import calorie_calculator

llm = OllamaLLM(model="ollama/mistral",base_url="http://ollama:11434")


def run_agent(prompt: str) -> str:
    agent = Agent(
        role="Nutritionist",
        goal="Create a personalized meal plan based on the provided user profile",
        backstory="A certified  nutritionist trained in sports science and metabolic calculations.",
        llm=llm,
        tools=[calorie_calculator],
        verbose=True,
    )

    task = Task(
        description=prompt,
        expected_output="Return a complete 7-day meal plan with macros and calories per day.",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )


    result = crew.kickoff()
    return str(result)
