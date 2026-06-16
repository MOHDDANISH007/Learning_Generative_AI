from typing import TypedDict, Annotated, Optional
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

class review(TypedDict):
    summary: Annotated[str, "The summary of the review"]
    Technologies: Annotated[list[str], "The technologies used in this field"]
    Advantages: Annotated[list[str], "The advantages of the product"]
    Disadvantages: Annotated[list[str], "The disadvantages of the product"]
    sentiment: Annotated[str, "The sentiment of the review"]
    Code : Annotated[Optional[str], "The code of the review"]


llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=2080,
    temperature=0.7
)


chatModel = ChatHuggingFace(llm=llm)
structured_Model = chatModel.with_structured_output(review)


# result = structured_Model.invoke("""what is AI?""")
result = structured_Model.invoke("what is PCA?")

# print(result)


print(f"Summary: {result['summary']}")
print(f"Technologies: {result['Technologies']}")
print(f"Advantages: {result['Advantages']}")
print(f"Disadvantages: {result['Disadvantages']}")
print(f"Sentiment: {result['sentiment']}")
print(f"Code: {result['Code']}")

# print(100*"-")


# print(f"Result keys is {result.keys()}")
# print(f"Result items is {result.items()}")