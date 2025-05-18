
import sys , os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'agents')))
import streamlit as st
import praw
from agents.ollamaLLM import ollama_query
def scraper_agent(query: str) -> str:
    clientId = st.secrets["reddit"]["client_id"]
    clientSecret = st.secrets["reddit"]["client_secret"]
    userAgent = st.secrets["reddit"]["user_agent"]


    reddit = praw.Reddit(client_id=clientId, client_secret=clientSecret, user_agent=userAgent)
    
    # Search across all subreddits
    posts = reddit.subreddit("all").search(query, sort="new", limit=50)

    post_data = "\n".join([f"Title: {post.title}\nText: {post.selftext}" for post in posts])
    
    print(post_data)
    prompt = f"""
    Analyze the following Reddit posts related to "{query}":
    {post_data}
    """
    result = ollama_query(prompt)
    return result


