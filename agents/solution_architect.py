
from agents.ollamaLLM import ollama_query

def solution_architect_agent(state: dict) -> dict:
    ideas = state.insights_data
    if not ideas:
         return {"error": "No insights data available"}
    prompt = f"""
    Based on the following user and market insights, design a potential MVP that Amazon can pilot.

    Insights:
    {ideas}

    Output:
    - One-liner description of the MVP
    - Target user segment
    - Key pain point addressed
    """
    solutions =  ollama_query(prompt)
    print("solutions",solutions)
    return {"mvp_idea": solutions}

