from google import genai
import os

def get_gemini_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_model():
    client = get_gemini_client()
    return client.models

def get_gemini_model_name():
    return "gemini-2.0-flash"