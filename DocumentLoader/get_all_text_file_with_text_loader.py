from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
import os

import glob

load_dotenv()


llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.7,
)

model = ChatHuggingFace(llm=llm)    


prompt = PromptTemplate(
    template="Generate a short and simple notes from the following text: {text}",
    input_variables=["text"]
)

outputParser = StrOutputParser()


# Load ALL text files in a folder
all_files = glob.glob("*.txt")  # Gets all .txt files
documents = []

for file in all_files:
    loader = TextLoader(file, encoding="utf-8")
    documents.extend(loader.load())  # Add to list

# Now documents has MULTIPLE documents
print(f"Total documents: {len(documents)}")

# Access each document by index
doc1 = documents[0]  # First file
doc2 = documents[1]  # Second file
doc3 = documents[2]  # Third file

for doc in documents:
    print(f"Processing document: {doc.metadata}")
    # You can access content here if needed
    # print(doc.page_content[:100])


chains = prompt | model | outputParser

response = chains.invoke({"text": doc1.page_content})
print(f"Response for first document: {response}")





# def function_of_document(doc):  # Fixed spelling
#     print(f"Processing document: {doc.metadata['source']}")
#     print(f"length of content: {len(doc.page_content)}")

# # FIX: Add list() to execute map
# result  = list(map(function_of_document, documents))
# print(f"Total documents processed: {(result)}")