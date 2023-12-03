import streamlit as st
import langchain_helper1 as lch
from langchain_helper1 import medical_cond_analysis
from langchain_helper1 import split_pdf_into_batches
import boto3
from openai import OpenAI
import boto3
import openai
import streamlit as st
import retrying
import PyPDF2
import boto3
import io
from openai import OpenAI
from PyPDF2 import PdfReader
# import pdb
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

st.title("Medical Condition")

medical_condition = st.sidebar.text_area(
    label="Enter the Medical Condition",
    max_chars=30
)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="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", type="password")
    # def analyze_text_batch(text_batch):
    #     # Make an API call to analyze the text batch
    #     response = openai.Completion.create(
    #         engine="davinci",
    #         prompt=text_batch,
    #         max_tokens=50,  # Adjust as needed
    #         n = 1  # You can request multiple completions for more insights
    #     )
    #     return response.choices[0].text

if medical_condition:
  if not openai_api_key:
   st.info("Please add your OpenAI API key to continue.")
   st.stop()

  bucket_name = 'policydocumentschiesta'
  common_string = medical_condition  # Specify the common string in file names
  batch_size = 4000
  openai.api_key = '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' 
  for text_batch in split_pdf_into_batches(bucket_name, common_string, batch_size):
    # analysis_result = analyze_text_batch(text_batch)
    response = medical_cond_analysis(medical_condition, text_batch)
    st.text(response['policy_analysis'])
