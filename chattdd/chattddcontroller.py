import os
from testgenerator import TestGenerator
from modelinitializer import ModelInitializer
from file_handler import write_to_file

class ChatTddController:
    def __init__(self, model):
        self.generator = TestGenerator(model)
        
    def ask_user_for_requirement(self):
        return input("Please provide a functional requirement: ")
    
    def handle_test_code_generated(self, test_code):
        file_name = "test_foo.py"
        write_to_file(test_code, file_name) 
        
    def run(self):
        functional_requirement = self.ask_user_for_requirement()
        response = self.generator.run(functional_requirement)
        
        code_word = response.get("code_word")
        test_code = response.get("test_code")
        comment = response.get("comment")

        if code_word in ["REJECT", "COMPLEX"]:
            print(f"Valid test couldn't be made for this requirement: {comment}")
        elif code_word in ["PASS", "OK"]:
            self.handle_test_code_generated(test_code)

if __name__ == "__main__":
    model_initializer = ModelInitializer()
    model = model_initializer.initialize_model()
    controller = ChatTddController(model)
    controller.run()
