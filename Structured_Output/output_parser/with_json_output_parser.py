from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import json

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY"),
    max_new_tokens=300,
    task="text-generation",
    temperature=0.7
)

model = ChatHuggingFace(llm=llm)


parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
    Generate many realistic student profile.

    Include the student's:
    name, email, age, gender, course, university,
    city, country, skills, hobbies, graduation year,
    and a short bio.

    {format_instructions}
    """,
    input_variables=[],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)
# chaining the llm with the prompt and parser
chain = prompt | model | parser

result = chain.invoke({})
print(result["students"])

# store this data into file

if not os.path.exists("student_profiles.json"):
    with open("student_profiles.json", "w", encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)
else:
    students = json.load(open("student_profiles.json", "r", encoding="utf-8"))


students.extend(result["students"])

with open("student_profiles.json", "w", encoding="utf-8") as f:
    json.dump(students, f, indent=2, ensure_ascii=False)
