# ============================================
# SIMPLE SEMANTIC CHUNKING - FOR LEARNING
# ============================================

from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

# Step 1: Our sample text (notice the two different topics)
text = """
Artificial Intelligence is changing the world.
Machine Learning is a subset of AI.
Recommendation Systems are used in Machine Learning and AI systems like Netflix and Amazon Recommendation Systems are based on Machine Learning.
Deep Learning is a subset of Machine Learning.
Neural Networks are used in Deep Learning.
Yesterday I went to the market.
I bought apples and bananas.
Then I came back home.
Today the weather is very nice.
Nepal is a beautiful country and I want to visit it one day in my life.
Austria is a beautiful country and I want to visit it one day in my life.
"""

print("="*60)
print("📚 SEMANTIC CHUNKING - SIMPLE EXAMPLE")
print("="*60)

print("\n📝 Original Text:")
print("-"*40)
print(text)
print("-"*40)

# Step 2: Create embeddings (converts text to numbers)
# This is like giving the computer a way to "understand" meaning
    # model_name="sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(
    model_name="Vsevolod/company-names-similarity-sentence-transformer"
)

# Step 3: Create the semantic splitter
# This will group similar sentences together
splitter = SemanticChunker(
    embeddings=embeddings,  # How to understand meaning
    breakpoint_threshold_type="percentile",  # How to decide where to split
    breakpoint_threshold_amount=30  # Sensitivity (higher = fewer chunks)
)

# Step 4: Split the text
chunks = splitter.create_documents([text])

# Step 5: See the results
print(f"\n✅ Created {len(chunks)} semantic chunks\n")

for i, chunk in enumerate(chunks, 1):
    print("="*50)
    print(f"CHUNK {i}")
    print("="*50)
    print(chunk.page_content)
    print()