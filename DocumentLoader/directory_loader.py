from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser

loader = DirectoryLoader(
    path="pdf",
    glob="*.pdf",
    recursive=True,
    loader_cls=PyMuPDFLoader,
    loader_kwargs={
        "mode": "single",                    # or "single"
        "pages_delimiter": "\n---PAGE BREAK---\n",           # or "page"
        "extract_images": True,             # correct name
        "images_parser": TesseractBlobParser(),  # correct name + object
        "images_inner_format": "text"       # optional
    }
)

docs = loader.load()
print(docs[0].metadata)

print("Total docs:", len(docs))

for i, doc in enumerate(docs, start=1):
    print(f"\n========== DOC {i} ==========")
    print(doc.page_content[:1500])
    print(doc.metadata)