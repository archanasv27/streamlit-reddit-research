# tasks/state.py
from typing import Optional
from pydantic import BaseModel

class WorkflowState(BaseModel):
    subreddit: Optional[str] = None
    scraped_data: Optional[str] = None
    insights_data: Optional[str] = None
    mvp_idea: Optional[str] = None
    risk_assessment: Optional[str] = None
    final_presentation: Optional[str] = None
