import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGING_FACE_API_KEY")

if HF_TOKEN is None:
    raise ValueError("HUGGING_FACE_API_KEY is not set")
else:
    print("Hugging Face API key is set")

client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN
)

video = client.text_to_video(
    "Ghost Recon Wildlands Gameplay video",
    model="Wan-AI/Wan2.1-T2V-14B",
)

videoPath = "video.mp4"

with open(videoPath, "wb") as f:
    f.write(video)

print(f"Video saved to {videoPath}")
