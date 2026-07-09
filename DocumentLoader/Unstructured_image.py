from langchain_community.document_loaders import UnstructuredImageLoader

loader = UnstructuredImageLoader(
    file_path= "screenshotimage.png", # your image path
    mode="single"
)

docs = loader.load()

print("Total documents:", len(docs))
print("\nContent:\n")
print(docs[0].page_content)
print("\nMetadata:\n")
print(docs[0].metadata)