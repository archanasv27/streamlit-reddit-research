import sys
import os
from typing import TypedDict
import langgraph as lg

# Fix path so we can import from 'agents'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import agent functions
from agents.scraper import scraper_agent
from agents.solution_architect import solution_architect_agent
from agents.risk_assessor import risk_assessor_agent
from agents.insights import insights_agent
from agents.presentor import presentation_agent


from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from langgraph.graph import StateGraph

# tasks/task.py
from langgraph.graph import StateGraph
from tasks.state import WorkflowState  # <-- Import this!
from pydantic import BaseModel

from agents.scraper import scraper_agent
from agents.solution_architect import solution_architect_agent
from agents.risk_assessor import risk_assessor_agent
from agents.insights import insights_agent
from agents.presentor import presentation_agent


def create_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("scraper", RunnableLambda(lambda state: {"scraped_data": scraper_agent(state.subreddit)}))
    graph.add_node("insights", insights_agent)
    graph.add_node("solution_architect", solution_architect_agent)
    graph.add_node("risk_assessor", risk_assessor_agent)
    graph.add_node("presentor", presentation_agent)

    graph.add_edge("scraper", "insights")
    graph.add_edge("insights", "solution_architect")
    graph.add_edge("solution_architect", "risk_assessor")
    graph.add_edge("risk_assessor", "presentor")

    graph.set_entry_point("scraper")
    graph.set_finish_point("presentor")

    return graph.compile()  

