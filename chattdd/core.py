import json
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv, find_dotenv


def initialize_model():
    load_dotenv(find_dotenv())  # Load .env file, if it exists
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        openai_api_key = input("Please enter your OpenAI API key: ")
        with open('.env', 'w') as env_file:
            env_file.write(f'OPENAI_API_KEY={openai_api_key}\n')
    model = ChatOpenAI(model_name="gpt-3.5-turbo")

    return model

def generate_function(model, input_description):
    template = """
    You are a code generator that follows all principles of Test Driven Development. 
    You adhere to PEP 8.
    Your task is to generate code, not to provide explanations or comments. 
    The user will prompt you with a required task. 
    Your reply will have five parts:
     1. a function name that reflects the function.
     2. the function in python code with includes if required. No comments. 
     3. a file name where we'll store the function.
     4. a pytest that test the function in python code with includes if required. No comments.
     5. a file name for the pytest test code.
     
     You will return this in a JSON format. Keys are: 
     "function_name", "function_code", "function_file_name", "test_code", "test_file_name"

    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", template), ("human", f"{input_description}")]
    )

    chain = prompt | model | StrOutputParser()
    result = chain.invoke({"input": input_description})
    output_json = json.loads(result) 
    return output_json