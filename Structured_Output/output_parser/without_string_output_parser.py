from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate


load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=300,
    task="text-generation",
    temperature=0.7
)

model = ChatHuggingFace(llm=llm)

# 1st prompt
promptTemplate1 = PromptTemplate(
    template="Write a detailed report on it : {topic}",
    input_variables=["topic"]
)


# 2nd prompt
promptTemplate2 = PromptTemplate(
    template="Write a 5 line summary on the following text. \n {text}",
    input_variables=["text"]
)   

# code
prompt1 = promptTemplate1.invoke("what is AI?")
# code
result1 = model.invoke(prompt1)

print(result1.content)
# code
prompt2 = promptTemplate2.invoke(result1.content)
# code
result2 = model.invoke(prompt2)

print(100*"-")

print(result2.content)