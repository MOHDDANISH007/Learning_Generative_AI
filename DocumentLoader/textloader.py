from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
import glob
import os



load_dotenv()

print(f"glob {glob}")
llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.7,
)

model = ChatHuggingFace(llm=llm)

# Create loader
cricketFile = TextLoader("cricket.txt", encoding="utf-8")

# Load the document
documents = cricketFile.load()

# source
print(documents[0].metadata)  # Print the source of the document


