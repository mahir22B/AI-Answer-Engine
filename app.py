import os
from openai import OpenAI
import requests
from dotenv import load_dotenv
import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

st.title("Your Own Answer Engine")
st.caption("Add Web")

# Load environment variables from a .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def do_web_search(full_user_prompt: str, num_results: int = 5):
    API_URL = os.getenv("TAVILY_API_KEY")
    payload = {
        "api_key": "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",
        "query": full_user_prompt,
        "search_depth": "basic",
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
        "max_results": num_results,
        "include_domains": [],
        "exclude_domains": []
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        all_results = "\n\n".join(item["content"] for item in data['results'])
        logging.info(f"Web search successful. Results: {all_results[:100]}...")
        return all_results
    except requests.RequestException as e:
        logging.error(f"Web search failed: {e}")
        return None

def query_openai(messages, functions=None):
    try:
        if functions:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                functions=functions,
                function_call="auto"
            )
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages
            )
        logging.info(f"OpenAI query successful. Response: {response.choices[0].message}")
        return response.choices[0].message
    except Exception as e:
        logging.error(f"OpenAI query failed: {e}")
        return None

def answer_with_search(question):
    functions = [
        {
            "name": "do_web_search",
            "description": "Searches the web for the user question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "full_user_prompt": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of search results to return"
                    }
                },
                "required": ["full_user_prompt"]
            }
        }
    ]
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. If you need current information to answer a question, use the do_web_search function."},
        {"role": "user", "content": question}
    ]
    response = query_openai(messages, functions)
    
    if response and hasattr(response, 'function_call'):
        logging.info(f"Function call detected: {response.function_call.name}")
        if response.function_call.name == "do_web_search":
            search_results = do_web_search(**eval(response.function_call.arguments))
            if search_results:
                messages.append({"role": "function", "name": "do_web_search", "content": search_results})
                messages.append({"role": "user", "content": f"Based on the search results, please answer the original question: {question}"})
                final_response = query_openai(messages)
                if final_response:
                    return final_response.content
    elif response:
        return response.content
    
    return "I'm sorry, but I couldn't generate a response at this time. Please try again later."

# Streamlit UI
question = st.text_input("Ask a question here", key="user_question")

if question:
    with st.spinner('Searching and generating answer...'):
        answer = answer_with_search(question)
    st.write(answer)

