from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    task="text-generation",
    max_new_tokens=300,
    temperature=0.7
)


# Step 1: Prompt
prompt = ChatPromptTemplate.from_template("Explain {topic} in very simple English")

# Step 2: Model
model = ChatHuggingFace(llm=llm)

# Step 3: Parser
parser = StrOutputParser()

# Step 4: Chain
chain = prompt | model | parser

# Step 5: Stream output
# for chunk in chain.stream({"topic": "Artificial Intelligence"}):
#     print(chunk, end="")

# for chunk in chain.stream({"topic": "Artificial Intelligence"}):
#     print("\n---CHUNK START---")
#     print((chunk))
#     print("---CHUNK END---")



for chunk in chain.stream({"topic": "Artificial Intelligence"}):
    print(chunk, end="", flush=False)