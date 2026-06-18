from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field   
from typing import Literal
import os

load_dotenv()

# Initialize the LLM with a valid Hugging Face model
llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",  # Use a valid model
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=1200,
    task="text-generation",
    temperature=0.7
)

# Define the sentiment model
class Sentiment(BaseModel):
    Sentiment: Literal["positive", "negative", "neutral"] = Field(description="The sentiment of the text")

# Initialize parsers
parser = StrOutputParser()
parser2 = PydanticOutputParser(pydantic_object=Sentiment)

# Prompt for sentiment classification
prompt1 = PromptTemplate(
    template="Classify the sentiment of the following text: {text} \n {format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": parser2.get_format_instructions()},
)

# Create the chat model
model = ChatHuggingFace(llm=llm)

# Chain for sentiment classification
classifier_chain = prompt1 | model | parser2

# Prompts for different sentiments
prompt2 = PromptTemplate(
    template="Write an appropriate response for positive sentiment: {text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template="Write an appropriate response for negative or neutral sentiment: {text}",
    input_variables=["text"]
)

# Branch chain based on sentiment
branch_chain = RunnableBranch(
    (lambda x: x.Sentiment == "positive", prompt2 | model | parser),
    (lambda x: x.Sentiment == "neutral", prompt3 | model | parser),
    (lambda x: x.Sentiment == "negative", prompt3 | model | parser),
    RunnableLambda(lambda x: "Could not find sentiment")
)

# Complete chain
chain = classifier_chain | branch_chain

def textFunction(text: str) -> str:
    """Process user input and return appropriate response based on sentiment"""
    try:
        result = chain.invoke({"text": text})
        return result
    except Exception as e:
        return f"Error processing your request: {str(e)}"

if __name__ == "__main__":
    print("🤖 Sentiment-Based Response System")
    print("-" * 40)
    userQuery = input("Enter your text: ")
    result = textFunction(userQuery)
    print("\n" + "=" * 40)
    print("Response:", result)
    print("=" * 40)