from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
load_dotenv()

client = InferenceClient(
    provider="scaleway",
    api_key=os.environ["HUGGING_FACE_API_KEY"],
)

sentences = [
    "I love dogs",
    "I like Cats",
    "The weather is very hot today"
]

embeddings = []

for sentence in sentences:
    embedding = client.feature_extraction(
        sentence,
        model="Qwen/Qwen3-Embedding-8B"
    )
    embeddings.append(embedding.squeeze())

print(f"Embeddings: {embeddings}")

def userQueryEmbedding(query):
    embedding = client.feature_extraction(
        query,
        model="Qwen/Qwen3-Embedding-8B"
    )
    UserEmbedding = embedding.squeeze()
    return UserEmbedding


userQuery = input("Ask me anything: ")
userQueryEmbedding = userQueryEmbedding(userQuery)

similarities = cosine_similarity([userQueryEmbedding], embeddings)

print(similarities)