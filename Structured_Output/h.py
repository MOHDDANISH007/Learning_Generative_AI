from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from pydantic import BaseModel, Field

# 1. Define the schema
class UserInfo(BaseModel):
    name: str = Field(description="The full name of the user")
    age: int = Field(description="The age of the user")

# 2. Load the Hugging Face model (requires HuggingFace API Token)
llm = HuggingFaceEndpoint(repo_id="meta-llama/Meta-Llama-3-8B-Instruct")
model = ChatHuggingFace(llm=llm)

# 3. Bind the schema
structured_model = model.with_structured_output(UserInfo)

# 4. Invoke the model
result = model.invoke("Extract the details: John Doe is 30 years old.")
print(result.name) # John Doe
