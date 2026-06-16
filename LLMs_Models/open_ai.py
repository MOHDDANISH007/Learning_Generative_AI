from langchain_openai import OpenAI
from dotenv import load_dotenv
# import google gemini from langchain_google_gemini import GoogleGemini
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
print(f"OpenAI API Key: {OPEN_AI_API_KEY}")

llm_openai = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.9, openai_api_key=OPEN_AI_API_KEY)

response = llm_openai.invoke("capital of France")
print(response)