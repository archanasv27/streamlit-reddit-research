from agents.ollamaLLM import ollama_query

def risk_assessor_agent(state: dict) -> dict:
    idea = state.mvp_idea 
    if not idea:
         return {"error": "No MVP idea available"}
    prompt = f"""
    Conduct a risk analysis for the following MVP/product idea, considering the dynamic tech and market environment Amazon operates in.

    Startup Idea:
    {idea}

    Evaluate and explain the following risks:
    - Market Risk (demand, timing, fit)
    - Technology Risk (feasibility, scalability)
    - Competitive Risk (existing players, defensibility)
    - Adoption Risk (user behavior, friction)
    """
    risks = ollama_query(prompt)
    return {"risk_assessment": risks}

