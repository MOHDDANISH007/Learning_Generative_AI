from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="moonshotai/Kimi-K2-Instruct-0905:novita",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=500,
    temperature=0.7
)

chatModel = ChatHuggingFace(llm=llm)

# result = chatModel.invoke("""what is AI?""")
result = chatModel.invoke("what is PCA?")

print(result)