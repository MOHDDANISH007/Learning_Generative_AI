from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    task="text-generation",
    max_new_tokens=300,
    temperature=0.7
)

model = ChatHuggingFace(llm=llm)

parser = StrOutputParser()

# -------------------------
# Prompt 1: Generate Joke
# -------------------------

prompt_generate_joke = PromptTemplate(
    template="Write a funny joke about {topic}.",
    input_variables=["topic"]
)

# -------------------------
# Prompt 2: Explain Joke
# -------------------------

prompt_explain = PromptTemplate(
    template="""
Explain the following joke in simple English.

Joke:
{joke}
""",
    input_variables=["joke"]
)

# -------------------------
# Joke Generator Chain
# -------------------------

joke_chain = (
    prompt_generate_joke
    | model
    | parser
)

# lambda function with runnablelamda

def count_word(text: str) -> int:
    return len(text.split())

count_words_runnable = RunnableLambda(count_word)

# -------------------------
# Parallel Chain
# -------------------------

parallel_chain = RunnableParallel(

    joke=RunnablePassthrough(),

    count_words=count_words_runnable,
    # count_words=RunnableLambda(count_word),

    explanation=(
        prompt_explain
        | model
        | parser
    )
)

final_chain = joke_chain | parallel_chain


# -------------------------
# Invoke Chain
# -------------------------

result = final_chain.invoke({"topic": "Python"})
print(f"length of the joke is {result['count_words']} words")

print(result)