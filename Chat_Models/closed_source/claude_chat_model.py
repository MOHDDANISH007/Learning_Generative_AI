# # import getpass  # Imports a module for secure password/input handling
# # import os       # Imports operating system interface module

# # # if "ANTHROPIC_API_KEY" not in os.environ:  # Checks if the API key exists in environment variables
# # #     os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")
# # #     # If not found, securely prompts user to enter it and stores it in environment variables


# # print(os.getcwd())  # Gets the current working directory
# # print(os.listdir())  # Lists the files in the current directory
# # # os.makedirs("parent/child") # Creates a new directory structure if it doesn't exist 
# # print(os.name)
# # print(os.cpu_count())
# # os.popen("ls")                # Run and capture output (older)


# # import getpass

# # # 1. getpass() - Most common (99% of usage)
# # password = getpass.getpass("Enter password: ")
# # api_key = getpass.getpass("API Key: ")

# # # 2. getuser() - Returns current login name
# # username = getpass.getuser()  # Returns "john_doe" or similar
# # print(f"Current user: {username}")



# import os 
# import getpass 

# if "ANTHROPIC_API_KEY" not in os.environ:
#     os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")


# from dotenv import load_dotenv

# load_dotenv()

# if not os.environ.get("DB Password"):
#     os.environ["DB Password"] = getpass.getpass("Enter your DB Password: ")


# def setup_config():
#     config = {}
#     config["user"] = getpass.getuser()
#     config["path"] = os.getcwd()
    
#     if not os.environ.get("SECRET_TOKEN"):
#         config["token"] = getpass.getpass("Your secret token: ")
    
#     return config


# config = setup_config()
# print(config)


import getpass
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()
# initialize with null for now
ANTHROPIC_API = None
if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")
    ANTHROPIC_API = os.getenv("ANTHROPIC_API_KEY")


print(f"Anthropic API key: {ANTHROPIC_API}...")

  # Print only the first 5 characters for security
model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",  # Note: Changed to a valid model name
    temperature=0.9,
    max_tokens=2048,
    anthropic_api_key=ANTHROPIC_API
)

# ✅ Use .invoke() method
response = model.invoke("What is the meaning of life?")
print(response.content)  # Use .content to get the text response
