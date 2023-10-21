from langchain.chat_models.openai import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.cache import InMemoryCache
from chattdd.extractvalues import extract_value
from tools import strip_extra_quotes


class TestGenerator:
    def __init__(self, model):
        self.llm = model
        self.code_word = None
        self.test_code = None
        self.comment = None

    def generate_test(self, functional_requirement):
        test_generator_template: str = """System message:\
        You are a very helpful python developer assistant and expert in test driven development with Pytest.\
        You will write one or more pytests for a function which solves the users requirements given below.\
        You will not include the function to be tested.
        Follow these standards:
        - Never repeat a test.
        - Add multiple tests when that makes sence, also negative tests.
        - Always provide entire file contents. Avoid suggesting like "maintain this unchanged".
        - Whenever you share a file version, it overwrites my previous knowledge of the file, becoming the new reference.
        - Prefer double quotes over single quotes.
        - Omit comments in application and test scripts.
        - The file you provide should begin with a comment specifying the full path to the current file.\
        You will generate a code_word field. If the requirement is too complex for a single function, then the code word should be 'COMPLEX'. In this case, don't return any code.\
        If the requirement fits in a single function that you can write tests for, then the code_word should be 'OK'.
        If the requirement is too complex for a single function, 
        No introduction or politeness. Your response MUST be a Python Dictionary in the following format:
            code_word: 'OK' or 'COMPLEX'.
            test_code: the entire contents of the file that contains the test function or functions, unless the requirement was too complex.
            comment: any comment you have about the test functionality

        Here is the functional requirements submitted to you:\
        {input}\

        Limit the reply to 2000 tokens. 
        """

        test_generator_prompt_template: PromptTemplate = PromptTemplate(
            input_variables=["input"], template=test_generator_template)
        test_generator_chain: LLMChain = LLMChain(
            llm=self.llm, output_key="generated_test", prompt=test_generator_prompt_template)

        reply = test_generator_chain.run({"input": functional_requirement})
        self.code_word = strip_extra_quotes(extract_value(reply, 'code_word'))
        self.test_code = strip_extra_quotes(extract_value(reply, 'test_code'))
        self.comment = strip_extra_quotes(extract_value(reply, 'comment'))
        
    def validate_test(self, functional_requirement):
        test_generator_verifyer_template: str = """Please pass or reject the following test code.\
        "
        {test_code}"\
        \
        All the following criterias (1-4) must be met to pass: \
        1 the file contains one or more tests that pytest can run.\
        2 the tests will actually test a function that meets the requirement: {input}\
        3 the test file should not include the function that solves the requirement {input}\
        4 most relevant scenario(s) are covered by the test(s).\

        If you choose to reject the test, you should suggest a new implementation of the entire test file, following the best practice for test driven developement with Pytest.\
        If you coose to pass the test, you shouldn't return any code at all, just place PASS in the code_word field.\
        No introduction or politeness. Your response should be in the following format, as a Python Dictionary:
        code_word: PASS if you return code, COMPLEX if the requirements are too complex.
        test_code: the entire contents of the new test file if you chose to reject the previous.
        comment: your thoughts on why the test was rejected or passed.

        """

        test_validator_prompt_template: PromptTemplate = PromptTemplate(
            input_variables=["input", "test_code" ], template=test_generator_verifyer_template)
        test_validator_chain: LLMChain = LLMChain(
            llm=self.llm, output_key="generated_test", prompt=test_validator_prompt_template)

        reply = test_validator_chain.run({"input": functional_requirement, "test_code": self.test_code})
        self.code_word = extract_value(reply, 'code_word')
        self.test_code = extract_value(reply, 'test_code')
        self.comment = extract_value(reply, 'comment')

    def run(self, functional_requirement):
        self.generate_test(functional_requirement)
        
        if self.code_word == "COMPLEX":
            return {
                "code_word": self.code_word,
                "test_code": self.test_code,
                "comment": self.comment
            }
        

        #TODO: validation step: 
        #self.validate_test(functional_requirement) <- pass code
        

        if self.code_word == "REJECT":
            # Run validate_test again with the returned test_code
            self.validate_test(functional_requirement)
            
            if self.code_word == "REJECT":
                return {
                    "code_word": self.code_word,
                    "test_code": None,
                    "comment": self.comment
                }


        return {
            "code_word": self.code_word,
            "test_code": self.test_code,
            "comment": self.comment
        }

if __name__ == "__main__":
    functional_requirement = "return a combined string output from string input s1 and string input s2"
    functional_requirement = "A function that takes a string as an input and returns a list with the occurrence of each word."
    functional_requirement = "return a random prime number between 100 and 1000"
    from modelinitializer import ModelInitializer
    model_initializer = ModelInitializer()
    model = model_initializer.initialize_model()
    generator = TestGenerator(model)
    response = generator.run(functional_requirement)
    print(response)