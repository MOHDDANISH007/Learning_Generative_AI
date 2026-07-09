from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredPDFLoader, PyPDFLoader

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
    """Generate a short, simple notes from the following text: {text} and do let me know is there any kind of images in the text or not make sure in the end or complete the response""",
    input_variables=["text"]
)

outputParser = StrOutputParser()

model = ChatHuggingFace(llm=llm)

loader = UnstructuredPDFLoader("comprehensive_sports_guide.pdf")

documents = loader.load()

# print(len(documents))
chains = prompt | model | outputParser

for doc in documents:
    response = chains.invoke({"text": doc.page_content})
    print(f"Response for document {doc.metadata['source']}: {response}")