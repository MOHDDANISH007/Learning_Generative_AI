from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=300,
    task="text-generation",
    temperature=0.7
)

model = ChatHuggingFace(llm=llm)

promptTemplate = PromptTemplate(
    template="Generate a short and simple notes from the following text: {text}",
    input_variables=["text"]
)

outputParser = StrOutputParser()

chains = promptTemplate | model | outputParser

print(f"Invoking the chain")
response = chains.invoke({"text": "The quick brown fox jumps over the lazy dog."})
print(f"Response: {response}")




