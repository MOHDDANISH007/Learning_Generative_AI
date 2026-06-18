from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import os

load_dotenv()

llm1 = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=1200,
    task="text-generation",
    temperature=0.7
)

llm2 = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=1200,
    task="text-generation",
    temperature=0.7
)

model1 = ChatHuggingFace(llm=llm1)
model2 = ChatHuggingFace(llm=llm2)

prompt1 = PromptTemplate(
    template="Generate a short and simple notes from the following text: {text}",
    input_variables=["text"]
)

prompt2 = PromptTemplate(
    template="Generate a 5 short question answers from the following text. \n {text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template="Merge the Provide the notes and quiz into a single document-> {notes} \n {quiz}",
    input_variables=["notes", "quiz"]
)

parser = StrOutputParser()

parallel = RunnableParallel({
    "notes": prompt1 | model1 | parser,
    "quiz": prompt2 | model2 | parser
})

# merge the notes and quiz
mergingChain = prompt3 | model1 | parser

FinalChain = parallel | mergingChain


def textFunction(text: str)-> str:
    return FinalChain.invoke({"text": text})


if __name__ == "__main__":
    print(textFunction("Tell Me What is Python? and how was invented it"))


# print("Printing How Chain Looks")
# FinalChain.get_graph().print_ascii()