
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader


textData ="""
My name is Danish
I am 22 years old

I live in Gurgaon
How are you?
"""


loader = DirectoryLoader(
    path="pdfs",
    glob="*.pdf",
    recursive=True,
    loader_cls=PyPDFLoader,
    loader_kwargs={"mode": "page"}
)

documents = loader.load()
print(f"Documents loaded: {len(documents)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separators=["\n\n", "\n", " ", ""]
)
# split documets into chunks
chunks = text_splitter.split_documents(documents)
# split text into chunks
# chunks = text_splitter.split_text(textData)


print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5], 1):   # first 5 only
    print(f"\nChunk {i}: {repr(chunk.page_content)}")