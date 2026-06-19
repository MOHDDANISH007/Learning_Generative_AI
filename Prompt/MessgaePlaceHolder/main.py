from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

# LLM
llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=2080,
    task="text-generation",
    temperature=0.7
)

chat = ChatHuggingFace(llm=llm)

# Chat history file
fileName = "/Users/mohddanish/Desktop/AI_Agentic_Langchain/LangChain_Models/Prompt/chat_history.json"
# fileName = "chat_history.json"

# Load existing chat history
if os.path.exists(fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        chat_history = json.load(f)
else:
    # make the file also
    with open(fileName, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)
    chat_history = []

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful customer support agent."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

chain = prompt | chat

while True:
    userQuery = input("\nEnter your query: ")

    if userQuery.lower() == "exit":
        print("Goodbye!")
        break

    if userQuery.lower() == "clear":
        chat_history = []

        with open(fileName, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=4)

        print("🗑️ Chat history cleared!")
        continue

    # Convert JSON history into LangChain messages
    messages = []

    for chat_item in chat_history:
        messages.append(
            HumanMessage(content=chat_item["userquery"])
        )

        messages.append(
            AIMessage(content=chat_item["response"])
        )

    # Invoke model
    result = chain.invoke({
        "chat_history": messages,
        "query": userQuery
    })

    print("\nAssistant:", result.content)

    # Save new conversation
    chat_history.append({
        "userquery": userQuery,
        "response": result.content,
        "timestamp": datetime.now().isoformat()
    })

    # Write updated history back to file
    with open(fileName, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4, ensure_ascii=False)