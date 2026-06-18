from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

# Validate API key exists
if not os.getenv("HUGGING_FACE_API_KEY"):
    print("Error: HUGGING_FACE_API_KEY not found in .env file")
    exit(1)

print("Initializing model...")

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=300,
    task="text-generation",
    temperature=0.7
)

model = ChatHuggingFace(llm=llm)

prompt = PromptTemplate(
    template="Generate 5 interesting facts about {topic}. List them with numbers.",
    input_variables=["topic"]
)

# Simple chain
chain = prompt | model | StrOutputParser()

print("Processing your request...")
try:
    response = chain.invoke({"topic": "Artificial Intelligence"})
    print("\n=== Success! ===\n")
    print(response)
    print("\n=== End of Response ===\n")
except Exception as e:
    print(f"Error occurred: {e}")