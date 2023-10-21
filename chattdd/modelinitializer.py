import os
import keyring
from chattdd.tools import load_config
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI


class ModelInitializer:
    
    @staticmethod
    def initialize_model(model_name=None):
        config = load_config()
        model_name = config['CHATTDD_MODEL']

        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            openai_api_key = keyring.get_password('openai', 'api_key')
            if not openai_api_key:
                openai_api_key = input("Please enter your OpenAI API key: ")
                keyring.set_password('openai', 'api_key', openai_api_key)

        os.environ['OPENAI_API_KEY'] = openai_api_key
        set_llm_cache(InMemoryCache())

        if model_name == 'text-davinci-003':
            model = OpenAI(model_name="text-davinci-003", max_tokens=3000, temperature=0, openai_api_key=openai_api_key)
        elif model_name == 'gpt-3.5-turbo':
            model = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=3000, temperature=0, openai_api_key=openai_api_key)
        elif model_name == 'gpt-4':
            model = ChatOpenAI(model_name="gpt-4", max_tokens=3000, temperature=0, openai_api_key=openai_api_key)
        else:
            raise ValueError(f'Unsupported model: {model_name}')

        return model
    

if __name__ == "__main__":
    # keyring.delete_password('openai', 'api_key') #UNCOMMENT FOR ENTERING NEW API KEY
    model = ModelInitializer().initialize_model()
