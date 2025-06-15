from langchain_ollama import OllamaLLM
from crewai import Agent, Task, Crew

def run_agent(prompt: str):
    llm = OllamaLLM(model="ollama/mistral")
    agent = Agent(
        role="Nutritionist",
        goal="Create a personalized plant-based meal plan",
        backstory="A certified sports nutritionist for vegan athletes.",
        llm=llm,
        verbose=False,
    )
    task = Task(
        description=prompt,
        expected_output="A detailed 7-day meal plan.",
        agent=agent
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=False)
    result = crew.kickoff()
    return result.output if hasattr(result, "output") else str(result)
