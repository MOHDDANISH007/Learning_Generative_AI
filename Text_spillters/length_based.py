from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader

loader = DirectoryLoader(
    path="pdfs",
    glob="*.pdf",
    recursive=True,
    loader_cls=PyMuPDFLoader,
    loader_kwargs={
        "mode": "page",
    }
)

splitter = CharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=0,
)

docs = loader.load()

chunks = splitter.split_documents(docs)

print(chunks[0])

# for i, chunk in enumerate(chunks, 1):
#     print(f"\nChunk {i}:")
#     print(chunk.page_content)