from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import random


load_dotenv()   
class myLLM:
    def __init__(self):
        print("LLM is Created")
        self.llm2 = HuggingFaceEndpoint(
            repo_id="moonshotai/Kimi-K2-Instruct-0905:novita",
            huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
            max_new_tokens=500,
            temperature=0.7
        )       


    def predict(self, prompt):
        response_list = [
            "Hello Danish, how are you!",
            "Capital of India is New Delhi",
            "IPL is the indian premier league",
            "AI is Artificial Intelligence",
            "ML is Machine Learning"
        ]
        # prompt
        print(f"prompt {prompt}")
        response = self.llm2.invoke(prompt)
        # generate a random number 
        randomIndex = random.randint(0, len(response_list) - 1)
        return response_list[randomIndex]
llm = myLLM()
llm.predict("Tell me what is the capital of India?")
class myPromptTemplate:
    def __init__(self, template, input_variables):
        print("Prompt Template is Created")
        self.template = template
        self.input_variables = input_variables

    # def format(self, input_dict):
    #     return self.template.format(**input_dict)
    def format(self, length, topic):
        return self.template.format(length=length, topic=topic)
prompt = myPromptTemplate(
    template="Write a {length} report on : {topic}",
    input_variables=["topic", "length"]
)
# print(prompt.template)
# print(prompt.format({"topic": "IPL", "length": "short"}))
print(prompt.format("medium", "AI"))

llm.predict(prompt.format("long", "AI"))







