import requests
from openai import OpenAI
import streamlit as st
def ollama_query(prompt: str, model: str = "mistral"):
    # print(f"Sending prompt to Ollama: {prompt}")

    # response = requests.post(
    #     "http://localhost:11434/api/generate",
    #     json={"model": model, "prompt": prompt, "stream": False},
    # )
    # print(response.json()["response"])
    # return response.json()["response"]  # Note: It's 'response' not 'output'
    try:
        apiKey =  st.secrets["openai"]["api_key"]
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=apiKey,
        )

        completion = client.chat.completions.create(
        
        extra_body={},
        model="meta-llama/llama-3.3-8b-instruct:free",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ]
        )
        # print("output : ",completion.choices[0].message.content)
        print(completion,"comp")

        return completion.choices[0].message.content
    except Exception as e:
        print("⚠️  LLM call failed:", e)
        return ""  
# print(ollama_query("who are you"))