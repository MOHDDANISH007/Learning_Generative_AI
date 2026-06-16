import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# =========================
# Chat Model Client
# =========================
chat_client = InferenceClient(
    api_key=os.environ["HUGGING_FACE_API_KEY"]
)

# =========================
# Get User Question
# =========================
if len(sys.argv) > 1:
    question = " ".join(sys.argv[1:])
else:
    question = input("Ask me anything: ")

print(f"\n🤔 Question: {question}")

# =========================
# Generate Text Response
# =========================
completion = chat_client.chat.completions.create(
    model="moonshotai/Kimi-K2-Instruct-0905:novita",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

answer = completion.choices[0].message.content

print(f"\n🤖 Answer:\n{answer}")

# =========================
# Image Generation Client
# =========================
image_client = InferenceClient(
    provider="together",
    api_key=os.environ["HUGGING_FACE_API_KEY"]
)

# =========================
# Generate Image
# =========================
image_prompt = "Generate the Ghost recon wildlands"

image = image_client.text_to_image(
    image_prompt,
    model="black-forest-labs/FLUX.1-schnell",
)

# =========================
# Save Image
# =========================
image_path = "generated_image.png"

image.save(image_path)

print(f"\n🖼️ Image saved as: {image_path}") 