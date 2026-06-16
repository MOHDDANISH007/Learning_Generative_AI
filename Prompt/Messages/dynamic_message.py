import os
from dotenv import load_dotenv

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="moonshotai/Kimi-K2-Instruct-0905:novita",
    huggingfacehub_api_token=os.environ["HUGGING_FACE_API_KEY"],
    max_new_tokens=500,
    temperature=0.7
)

chat = ChatHuggingFace(llm=llm)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {domain} expert."),
    ("human", "Explain in simple English: {question}")
])

chat_history = []

domain = input("Enter domain (e.g., Programming, AI, Math): ")

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    messages = prompt.format_messages(
        domain=domain,
        question=question
    )

    final_messages = chat_history + messages

    response = chat.invoke(final_messages)

    print(f"AI: {response.content}")

    chat_history.append(
        HumanMessage(content=question)
    )

    chat_history.append(
        AIMessage(content=response.content)
    )


print(f"AI Chat History {chat_history}")

