from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableBranch, RunnableLambda, RunnablePassthrough

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",  # This repo doesn't exist - consider using a real model
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.7,
)

model = ChatHuggingFace(llm=llm)

prompt1 = PromptTemplate(
    template="""
Write a detailed report on the topic {topic} and the length should be {length}.
""",
    input_variables=["topic", "length"]
)

prompt2 = PromptTemplate(
    template="""
Summarize the following report:

{report}
""",
    input_variables=["report"]  # Changed from "topic" to "report"
)

def should_summarize(report: str) -> bool:
    word_count = len(report.split())  # Better to count words, not characters
    print(f"Report word count: {word_count}")
    
    # Summarize if report has more than 100 words
    if word_count >= 100:
        print("Report is long enough - summarizing...")
        return True
    else:
        print("Report is short - no summarization needed")
        return False

# Create runnable for the condition
should_summarize_runnable = RunnableLambda(should_summarize)

# Report generation chain
report_generator_chain = RunnableSequence(
    prompt1, 
    model,
    StrOutputParser()
)

# Branch chain - if report is long, summarize it; otherwise, pass through
branch_chain = RunnableBranch(
    (should_summarize_runnable, prompt2 | model | StrOutputParser()),
    RunnablePassthrough()  # This will pass through the report as-is
)

# Final chain: generate report, then branch based on length
final_chain = report_generator_chain | branch_chain

print("Invoking the final chain...")
response = final_chain.invoke({
    "topic": "The quick brown fox jumps over the lazy dog.",
    "length": "70 words"  # Changed from "100" to "100 words" for clarity
})

print(f"\nFinal Response:\n{response}")