# prompt.py - WITH BOTH GEMINI AND KIMI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import streamlit as st
import os

load_dotenv()

# ============ GET API KEYS ============
GOOGLE_GEMINI_KEY = os.getenv("GOOGLE_GEMINI_KEY") or os.getenv("GOOGLE_API_KEY")
HF_API_KEY = os.getenv("HUGGING_FACE_API_KEY") or os.getenv("HF_TOKEN")
print(f"hugging face api key: {HF_API_KEY}")

# ============ INITIALIZE KIMI (Hugging Face) ============
if HF_API_KEY:
    kimi_client = InferenceClient(api_key=HF_API_KEY)
else:
    st.warning("⚠️ Hugging Face API key not found. Kimi model disabled.")

# ============ INITIALIZE GOOGLE GEMINI ============
if GOOGLE_GEMINI_KEY:
    google_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Use working model
        temperature=0.9,
        google_api_key=GOOGLE_GEMINI_KEY
    )
else:
    st.error("❌ Google Gemini API Key not found!")
    st.stop()

# ============ STREAMLIT UI ============
st.header("🔬 Research Tools")

# Model selection
model_choice = st.radio("Choose Model:", ["Google Gemini", "Kimi (Hugging Face)"])

paper_input = st.selectbox("Select a paper:", [
    "Attention is All You Need",
    "The Transformer", 
    "Language Models are Unsupervised Multitask Learners",
    "Exploring the Limits of Transfer Learning at Scale"
])

style_input = st.selectbox("Select Explanation style:", [
    "Beginner Friendly",
    "Technical",
    "Code-Oriented",
    "Mathematical-Oriented"
])

length_input = st.selectbox("Select Length:", [
    "Short",
    "Medium",
    "Long"
])

# Combine selections into a prompt
if st.button("Submit"):
    with st.spinner(f"Generating response with {model_choice}..."):
        prompt = f"""
        Explain the paper '{paper_input}' in a {style_input.lower()} style.
        Keep the explanation {length_input.lower()} in length.
        Focus on the key contributions and concepts.
        """
        
        try:
            if model_choice == "Google Gemini":
                # Use Google Gemini
                # ch
                result = google_llm.invoke(prompt)
                st.write("### 📝 Result (Gemini):")
                st.write(result.content)
                
            elif model_choice == "Kimi (Hugging Face)":
                # Use Kimi model
                if not HF_API_KEY:
                    st.error("❌ Hugging Face API key not configured!")
                else:
                    completion = kimi_client.chat.completions.create(
                        model="moonshotai/Kimi-K2-Instruct-0905:novita",
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.7
                    )
                    st.write("### 📝 Result (Kimi):")
                    st.write(completion.choices[0].message.content)
                    
        except Exception as e:
            st.error(f"Error: {e}")