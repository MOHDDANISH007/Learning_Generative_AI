from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

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
    template="""
Generate short and simple notes from the following text:

{text}

Also tell me clearly whether image text was also extracted from the PDF.
""",
    input_variables=["text"]
)

output_parser = StrOutputParser()

loader = PyMuPDFLoader(
    file_path="text_image_document.pdf",
    mode="page",                     # page-wise is better for learning
    extract_images=True,             # extract images
    images_parser=TesseractBlobParser(),   # OCR on extracted images
)

documents = loader.load()

print("Number of documents:", len(documents))

for i, doc in enumerate(documents):
    print(f"\n========== PAGE {i+1} ==========")
    print(doc.page_content[:1000])   # see what text came

chain = prompt | model | output_parser

result = chain.invoke({"text": documents[0].page_content})

print("\nFinal Output:\n")
print(result)