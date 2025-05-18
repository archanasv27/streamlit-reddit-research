from agents.ollamaLLM import ollama_query

def insights_agent(state: dict) -> dict:
    print("statessssss",state)
    data = state.scraped_data 

    prompt = f"""
    Analyze the following startup- and customer-related discussions extracted from Reddit, Hacker News, and LinkedIn. 
    Classify each insight into one of the following actionable categories:
    - Customer Pain Points Amazon Can Solve
    - Hidden Product or Service Opportunities
    - Emerging Market or Behavioral Trends
    Your goal is to identify signals Amazon could act on for new products, category expansion, or investment decisions.

    {data}
    """
    summary_text = ollama_query(prompt)


    return {"insights_data": summary_text}
