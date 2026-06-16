from langchain_openai import OpenAI
from dotenv import load_dotenv
# import google gemini from langchain_google_gemini import GoogleGemini
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY")
print(f"Google Gemini API Key: {GOOGLE_GEMINI_KEY}")


# for google gemini

# Initialize Google Gemini
google_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # or "gemini-1.5-pro"
    temperature=0.9,
    google_api_key=GOOGLE_GEMINI_KEY  # This is the correct parameter name
)

# Test the model
response = google_llm.invoke("How is Elon Musk and what his age?")
print(f"\n📝 Response: {response.content}")