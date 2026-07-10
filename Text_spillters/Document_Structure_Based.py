from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.document_loaders import DirectoryLoader, BSHTMLLoader, TextLoader

# Load documents
loader = DirectoryLoader(
    path=".",
    glob="*.html",
    recursive=True,
    loader_cls=BSHTMLLoader
)

loaderPythonCode = DirectoryLoader(
    path="code",
    glob="*.py",
    recursive=True,
    loader_cls=TextLoader
)

loaderMarkDown = DirectoryLoader(
    path=".",
    glob="*.md",
    recursive=True,
    loader_cls=TextLoader
)

docs = loader.load()
pythonDocs = loaderPythonCode.load()
markdownDocs = loaderMarkDown.load()

print(f"HTML docs loaded: {len(docs)} files")
print(f"Python docs loaded: {len(pythonDocs)} files")
print(f"Markdown docs loaded: {len(markdownDocs)} files")


# Create splitters
splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.HTML,
    chunk_size=100,
    chunk_overlap=0
)

splitterPython = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=400,
    chunk_overlap=0
)

splitterMarkdown = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size=400,
    chunk_overlap=0
)


# Split documents
chunks = splitter.split_documents(docs)
chunksPython = splitterPython.split_documents(pythonDocs)
chunksMarkdown = splitterMarkdown.split_documents(markdownDocs)

print(f"\nTotal HTML chunks: {len(chunks)}")
print(f"Total Python chunks: {len(chunksPython)}")
print(f"Total Markdown chunks: {len(chunksMarkdown)}")


# pythonCode
# for i, chunk in enumerate(chunksPython, 1):
#     print(f"\n{'='*40}")
#     print(f"HTML CHUNK #{i}")
#     print(f"{'='*40}")
#     print(f"📏 Length: {len(chunk.page_content)} chars")
#     print(f"📝 Content:\n{chunk.page_content}")
#     print(f"📚 Metadata: {chunk.metadata}")



# Markdown
for i, chunk in enumerate(chunksMarkdown, 1):
    print(f"\n{'='*40}")
    print(f"HTML CHUNK #{i}")
    print(f"{'='*40}")
    print(f"📏 Length: {len(chunk.page_content)} chars")
    print(f"📝 Content:\n{chunk.page_content}")
    print(f"📚 Metadata: {chunk.metadata}")



