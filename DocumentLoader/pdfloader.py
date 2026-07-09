from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser

import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="zai-org/GLM-5.2",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.7,
)
prompt = PromptTemplate(
    template=
    """Generate a short and simple notes from the following text: {text}""",
    input_variables=["text"]
)

outputParser = StrOutputParser()

model = ChatHuggingFace(llm=llm)

loader = PyPDFLoader("comprehensive_sports_guide.pdf")

documents = loader.load()

# print(len(documents))
chains = prompt | model | outputParser
for doc, i in zip(documents, range(len(documents))):
    response = chains.invoke({"text": doc.page_content})
    print(f"Response for document {i} : {response}")
# response = chains.invoke({"text": documents[0].page_content})
# print(f"Response for first document: {response}")