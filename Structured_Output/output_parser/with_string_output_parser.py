from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


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

parser = StrOutputParser()


chain = promptTemplate1 | model | parser | promptTemplate2 | model | parser

result = chain.invoke("what is AI?")

print(result)

