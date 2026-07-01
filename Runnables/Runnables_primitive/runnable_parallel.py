from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from pydantic import BaseModel, Field 
from langchain_core.output_parsers import PydanticOutputParser

import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    task="text-generation",
    max_new_tokens=2080,
    temperature=0.7
)

# taking out the response from the LLM properly 
class Summary(BaseModel):
    summary: str = Field(description="The summary of the review")

class Advantages(BaseModel):
    advantages:list[str] = Field(description="The advantages of the product")

class Disadvantages(BaseModel):
    disadvantages:list[str] = Field(description="The disadvantages of the product")

summary_parser = PydanticOutputParser(
    pydantic_object=Summary
)


advantages_parser=PydanticOutputParser(
    pydantic_object=Advantages
)

disadvantages_parser=PydanticOutputParser(
    pydantic_object=Disadvantages
)

summary_prompt = PromptTemplate(
    template="""
Generate only the summary.

{format_instructions}

Topic:
{topic}
""",
    input_variables=["topic"],
    partial_variables={
        "format_instructions":
        summary_parser.get_format_instructions()
    }
)

advantages_prompt = PromptTemplate(
    template="""
Generate only the advantages.

{format_instructions}

Topic:
{topic}
""",
    input_variables=["topic"],
    partial_variables={
        "format_instructions":
        advantages_parser.get_format_instructions()
    }
)


disadvantages_prompt = PromptTemplate(
    template="""
Generate only the disadvantages.

{format_instructions}

Topic:
{topic}
""",
    input_variables=["topic"],
    partial_variables={
        "format_instructions":
        disadvantages_parser.get_format_instructions()
    }
)

model = ChatHuggingFace(llm=llm)

chain = RunnableParallel(
    # again over here we creating sequential chains but with parallel chains, which means these chains(first, second, third) will run in parallel..
    
    first=summary_prompt | model | summary_parser,
    second=advantages_prompt | model | advantages_parser,
    third=disadvantages_prompt | model | disadvantages_parser
)

print("Invoking chain...\n")

response = chain.invoke({
    "topic": "Artificial Intelligence",
    "length": "100 words"
})

print(response)