from agents.ollamaLLM import ollama_query

def presentation_agent(state:dict) -> dict:
   
    analysis = (
        getattr(state, "risk_assessment", None) or
        getattr(state, "mvp_idea", None) or
        getattr(state, "insights_data", None) or
        "No analysis provided."
    )

    prompt = f"""
    Summarize the following market analysis into a decision-ready format for Amazon's business strategy team.Do not mention the name Amazon anywhere keep it generic.
    

    Include:
    - Key customer pain points
    - Potential opportunity areas
    - MVP suggestion (if any)
    - Risk summary

    Format as bullet points or a structured table for executive review.

    {analysis}
    """
    presenter = ollama_query(prompt)
    return {"final_presentation": presenter}
