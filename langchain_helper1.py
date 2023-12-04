import boto3
import openai
import streamlit as st
import PyPDF2
import openai
import boto3
import io
import retrying
from openai import OpenAI
from PyPDF2 import PdfReader
# import pdb
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

from dotenv import load_dotenv

load_dotenv()
# client = OpenAI()
client = OpenAI(openai_api_key='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')


def split_pdf_into_batches(bucket_name, common_string, batch_size):

 access_key = 'AKIARRRXC4SUHUDGBD67'
 secret_key = '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'

 s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
 try:
        # List objects in the S3 bucket that match the common string
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=common_string)

        if 'Contents' in response:
            # Iterate through the objects and read their content
            for obj in response['Contents']:
                file_name = obj['Key']
                # Read the file content
                response = s3.get_object(Bucket=bucket_name, Key=file_name)
                file_content = response['Body'].read()
                # Open the PDF file
                pdf_file = io.BytesIO(file_content)
                pdf_reader = PdfReader(pdf_file)

                # Initialize variables
                total_pages = len(pdf_reader.pages)
                current_page = 0

                while current_page < total_pages:
                    # Create a batch of text
                    text_batch = ''
                    while current_page < total_pages and len(text_batch) < batch_size:
                        page = pdf_reader.pages[current_page]
                        text_batch += page.extract_text()
                        current_page += 1

                    yield text_batch

                pdf_file.close()

 except Exception as e:
        print(e)
   
@retrying.retry(wait_fixed=1000, stop_max_attempt_number=3)  # Retry 3 times with a 1-second delay between retries   
def medical_cond_analysis(medical_condition, text_batch, openai_api_key):
    llm = OpenAI(temperature=0.7, openai_api_key= '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' )

    prompt_template_name = PromptTemplate(
        input_variables=['medical_condition' , 'text_batch'],
        template="I am a Hospital Medical Policy Analyst {medical_condition}. The {medical_condition} is for a patient. Consider the medical policy documents data from {text_batch}. As a medical policy analyst, I need to perform a meticulous and detailed comparison of medical policies pertaining to varicose across multiple insurance providers. Please structure the information into a well-organized table. Ensure that the data gathered is highly accurate and specific. The comprehensive comparison should encompass the following fields: Policy Number: This field should contain the unique identifier associated with each policy. Title: Include the official title as mentioned in the policy documents. Policy Criteria: Age Criteria: Document any age-related requirements for policy coverage. Specific Criteria for Medical Necessity: Elaborate on the particular conditions or prerequisites for the policy to be applicable. Insurance Company Name: List all insurance companies that offer the policy, especially if there are multiple providers. Insurance Type: Specify the type of insurance, such as Commercial, Medicaid, Traditional Medicare, or Medicare Advantage. Service Type: Categorize the policy based on service type, whether it falls under Medical, Pharmacy, or Specialty Drug (Medical Benefits). Status: Clearly indicate the current status of the policy, whether it's Active, Archived, or a Future policy. Link to Policy: Provide a direct link or reference to the policy document, typically in the form of a PDF file. Effective Date: Note the date when the policy officially took effect. Next Review: Mention the scheduled date for the next policy review. Last Review: Include the date of the most recent policy review. Guideline Source: If multiple sources contribute to the policy, cite them appropriately. States Covered: Enumerate the geographic regions or states where the policy applies. Needs Prior Authorization: Specify whether the policy necessitates prior authorization (Yes/No). Exclusions/Limitations: Describe any exclusions or limitations outlined in the policy. Coverage Period: Provide the precise start and end dates of the coverage period. Related Policies: Identify and document any policies that are linked or relevant to this particular policy. Note that some policies may not provide information for each category. Where this occurs, please indicate 'Not specified' in the relevant sections of the table."
    )

    # pdb.set_trace()
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="policy_analysis")

    response = name_chain({'medical_condition': medical_condition, 'text_batch': text_batch})

    return response 

def __init__(self, openai_api_key: str):
    self.openai_api_key = openai_api_key    

# if __name__ == '__main__':
    # print(medical_cond_analysis('Cochlear Implantation'))
