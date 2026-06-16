# pydantic code

# from typing import TypedDict, Annotated, Optional
# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
# from dotenv import load_dotenv
# import os
# from pydantic import BaseModel, Field

# load_dotenv()

# class review(BaseModel):
#     summary: str = Field(description="The summary of the review")
#     Technologies: list[str] = Field(description="The technologies used in this field")
#     Advantages: list[str] = Field(description="The advantages of the product")
#     Disadvantages: list[str] = Field(description="The disadvantages of the product")
#     sentiment: str = Field(description="The sentiment of the review")
#     Code : Optional[str] = Field(description="The code of the review")


# llm = HuggingFaceEndpoint(
#     repo_id="openai/gpt-oss-120b",
#     huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
#     max_new_tokens=2080,
#     temperature=0.7
# )




# chatModel = ChatHuggingFace(llm=llm)
# structured_Model = chatModel.with_structured_output(review)


# result = structured_Model.invoke("""what is AI?""")
# # result = structured_Model.invoke("what is PCA?")

# print(result)

# print(100*"-")


# print(f"Result keys is {result.keys()}")
# print(f"Result items is {result.items()}")

 
# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional

# class Person(BaseModel):
#     first_name: str
#     last_name: str
#     email: EmailStr
#     age: int  # Removed the comma
#     cgpa: Optional[float] = Field(ge=0, le=10)  # ge=0 (greater than or equal), le=10 (less than or equal)

# try:
#     newPerson = Person(
#         first_name="John",
#         last_name="Doe",
#         email="john.doe@example.com",  # Email is required!
#         age=30,  # Added comma here
#         cgpa=9.5
#     )
#     print(newPerson)
#     print(f"\nName: {newPerson.first_name} {newPerson.last_name}")
#     print(f"Email: {newPerson.email}")
#     print(f"Age: {newPerson.age}")
#     print(f"CGPA: {newPerson.cgpa}")

# except Exception as e:
#     print(f"Error: {e}")







from pydantic import BaseModel, Field
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class review(BaseModel):
    summary: str = Field(description="The summary of the review")
    Technologies: list[str] = Field(description="The technologies used in this field")
    Advantages: list[str] = Field(description="The advantages of the product")
    Disadvantages: list[str] = Field(description="The disadvantages of the product")
    sentiment: str = Field(description="The sentiment of the review")
    Code: Optional[str] = Field(description="The code of the review")

# Use Gemini (supports with_structured_output)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_GEMINI_KEY"),
    temperature=0.7
)

# This WILL work
structured_llm = llm.with_structured_output(review)
result = structured_llm.invoke("what is AI?")

print(f"Summary: {result.summary}")
print(f"Technologies: {result.Technologies}")
print(f"Advantages: {result.Advantages}")
print(f"Disadvantages: {result.Disadvantages}")
print(f"Sentiment: {result.sentiment}")