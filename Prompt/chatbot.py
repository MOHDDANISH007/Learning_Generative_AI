import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from datetime import datetime

load_dotenv()

client = InferenceClient(
    api_key=os.environ["HUGGING_FACE_API_KEY"],
)

# File to store chat history
CHAT_FILE = "chat_history.json"

def load_chat_history():
    """Load chat history from file"""
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(history):
    """Save chat history to file"""
    with open(CHAT_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def format_history_for_ai(history):
    """Convert stored history into format for AI context"""
    messages = []
    for item in history:
        messages.append({"role": "user", "content": item["userquery"]})
        messages.append({"role": "assistant", "content": item["response"]})
    return messages

# Load existing chat history
chat_history = load_chat_history()

if chat_history:
    print(f"📚 Loaded {len(chat_history)} previous conversations from {CHAT_FILE}")
    print("Previous chats:")
    for i, chat in enumerate(chat_history[-3:], 1):  # Show last 3
        print(f"  {i}. You: {chat['userquery'][:50]}...")
    print()

# Main conversation loop
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break

    if user_input.lower() == "clear":
        chat_history = []
        save_chat_history(chat_history)
        print("🗑️ Chat history cleared!")
        continue
    
    # Prepare messages with full conversation history
    messages = format_history_for_ai(chat_history)
    messages.append({"role": "user", "content": user_input})
    
    print(f"🤔 Thinking... (Context includes {len(chat_history)} previous messages)")
    
    response = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct-0905:novita",  # Changed to working model
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    
    ai_response = response.choices[0].message.content
    
    # Store in history
    chat_history.append({
        "userquery": user_input,
        "response": ai_response,
        "timestamp": datetime.now().isoformat()
    })
    # Save to file immediately
    save_chat_history(chat_history)
    
    print(f"🤖 AI: {ai_response}")
    print(f"💾 Saved to {CHAT_FILE}")

print(f"\n👋 Goodbye! {len(chat_history)} conversations saved to {CHAT_FILE}")