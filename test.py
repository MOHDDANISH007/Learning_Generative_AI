import langchain
import os 
import openai
import numpy as np
import anthropic
import transformers
import huggingface_hub
from sklearn import __version__ as sckit_learn_version
import sys



# print("Installed package versions:")
# print(100*"-")
# print(f"LangChain version: {langchain.__version__}")
# print(f"OpenAI version: {openai.__version__}")
# print(f"NumPy version: {np.__version__}")
# print(f"LangChain-Anthropic version: {anthropic.__version__}")
# print(f"Transformers version: {transformers.__version__}")
# print(f"Hugging Face Hub version: {huggingface_hub.__version__}")
# print(f"Scikit-learn version: {sckit_learn_version}")


# print(os.path.exists(".env"))

print(sys.argv) 
print(sys.argv[1:])
print(sys.platform)
print(sys.version)
print(os.curdir)
print(sys.path)