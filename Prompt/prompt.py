from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate,load_prompt

load_dotenv()


st.header("Research Tools")


user_input = st.text_input("Enter your prompt:")

if st.button("Submit"):
    st.text("some random text")
