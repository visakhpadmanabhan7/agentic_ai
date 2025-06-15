from langchain_ollama import OllamaLLM

def run_llm(prompt: str):
    llm = OllamaLLM(model="mistral", base_url="http://host.docker.internal:11434")
    response = ""
    for chunk in llm.stream(prompt):
        response += chunk
    return response