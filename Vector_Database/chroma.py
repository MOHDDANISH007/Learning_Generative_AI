from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.schema import Document
from langchain_core.documents import Document 
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="Vsevolod/company-names-similarity-sentence-transformer"
)


doc1 = Document(
    page_content="Virat Kohli is one of the most successful and consistent batsmen in IPL history. Know for his aggressive batting style.",
    metadata={"team":"Royal Challengers Banglore"},
)


doc2 = Document(
    page_content="Rohit Sharma is one of the most successful and consistent batsmen in IPL history. Known for his consistent batting style.",
    metadata={"team":"Mumbai Indians"},
)

doc3 = Document(
    page_content="KL Rahul is one of the most successful and consistent batsmen in IPL history. Known for his consistent batting style.",
    metadata={"team":"Royal Challengers Banglore"},
)


doc4 = Document(
    page_content="Shikhar Dhawan is one of the most successful and consistent batsmen in IPL history. Known for his consistent batting style.",
    metadata={"team":"Royal Challengers Banglore"},
)

doc5 = Document(
    page_content="MS Dhoni is one of the most successful and consistent batsmen in IPL history. Known for his consistent batting style.",
    metadata={"team":"Chennai Super Kings"}
)

docs = [doc1, doc2, doc3, doc4, doc5]


embeddings = HuggingFaceEmbeddings(
    model_name="Vsevolod/company-names-similarity-sentence-transformer"
)

# vector_store = Chroma(
#     collection_name="ipl_batsmen",
#     embedding_function=embeddings,
#     persist_directory="chrom_db"
# )

vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="ipl_batsmen",
    persist_directory="chrom_db",
)

# vector_store.add_documents(docs)

# get collection or documents

print(
    vector_store.get(
        include=["embeddings"],
    )
)


results = vector_store.similarity_search(
    query="MS Dhoni",
    k=2
)

# results_score = vector_store.similarity_search_with_score(
#     query="MS Dhoni",
# )

print(results)

documents = result = vector_store.get(
    include=["documents"]
)
print(result["ids"])