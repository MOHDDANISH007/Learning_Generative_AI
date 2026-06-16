from dotenv import load_dotenv
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
    max_tokens=2048,
    google_api_key=GOOGLE_GEMINI_KEY  # This is the correct parameter name
)

# Test the model
response = google_llm.invoke("Suggest me the name of 10 Indian peoples names?")
print(f"\n📝 Response: {response.content}")