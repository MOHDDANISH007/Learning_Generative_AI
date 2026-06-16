# message.py - Using LangChain messages with LangChain's ChatHuggingFace
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

# Create the Hugging Face endpoint
llm = HuggingFaceEndpoint(
    repo_id="moonshotai/Kimi-K2-Instruct-0905:novita",
    huggingfacehub_api_token=os.environ["HUGGING_FACE_API_KEY"],
    max_new_tokens=500,
    temperature=0.7
)

# Wrap it with ChatHuggingFace to use LangChain messages
chat = ChatHuggingFace(llm=llm)

# ✅ Now you CAN use LangChain message objects!
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?")
]

# Get response
response = chat.invoke(messages)

while True:
    userQuery = input("Enter your query: ")
    if userQuery.lower() == "exit":
        break
    messages.append(HumanMessage(content=userQuery))
    response = chat.invoke(messages)
    # add AI response to messages
    messages.append(AIMessage(content=response.content))

    print(f"AI: {response.content}")


print("\nConversation history:")
for msg in messages:
    print(f"{msg.type}: {msg.content}...")