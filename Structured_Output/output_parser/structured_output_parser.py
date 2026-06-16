# from pydantic import BaseModel, Field
# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load environment variables from .env file

# llm = HuggingFaceEndpoint(
#     repo_id="google/gemma-2-2b-it",
#     huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
#     max_new_tokens=800,
#     task="text-generation",
#     temperature=0.7
# )

# model = ChatHuggingFace(llm=llm)

# class Movie(BaseModel):
#     """A movie with details."""
#     title: str = Field(description="The title of the movie")
#     year: int = Field(description="The year the movie was released")
#     director: str = Field(description="The director of the movie")
#     rating: float = Field(description="The movie's rating out of 10")

# model_with_structure = model.with_structured_output(Movie)

# response = model_with_structure.invoke("Provide details about the movie Inception")
# print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)






from pydantic import BaseModel, Field
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",  # Better for instructions
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=800,
    task="text-generation",
    temperature=0.7
)

model = ChatHuggingFace(llm=llm)

class Movie(BaseModel):
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")
    director: str = Field(description="The director of the movie")
    rating: float = Field(description="The movie's rating out of 10")

# parser = JsonOutputParser(pydantic_object=Movie)
parser = PydanticOutputParser(pydantic_object=Movie)

prompt = PromptTemplate(
    template="""You are a helpful assistant. Answer the user's query with a JSON object.

{format_instructions}

Query: {query}

Response:""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

try:
    response = chain.invoke({"query": "Provide details about the movie Inception"})
    print("Success!")
    print(response)
except Exception as e:
    print(f"Error: {e}")