import json
import os
import keyring
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from dotenv import load_dotenv, find_dotenv


def initialize_model():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        openai_api_key = keyring.get_password('openai', 'api_key')
        if not openai_api_key:
            openai_api_key = input("Please enter your OpenAI API key: ")
            keyring.set_password('openai', 'api_key', openai_api_key)
    
    os.environ['OPENAI_API_KEY'] = openai_api_key
    set_llm_cache(InMemoryCache())
    model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, verbose=True)
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