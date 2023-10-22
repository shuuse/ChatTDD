
# ChatTDD

ChatTDD is a utility designed to help developers create Test-Driven Python code using Langchain and OpenAI. By entering a description of the functionality you need, ChatTDD will generate code for that function based on a test. 

## Installation

To install ChatTDD, ensure you have Python 3.9 installed, then run the following command:

```markdown
pip install ChatTDD
```

## Configuration

Before using ChatTDD, you'll need to have an OpenAI API key. If you don't have one, you can obtain it from [OpenAI](https://beta.openai.com/signup/). Remember, using your api key with ChatTDD or any other client will come with a cost to you - so be warned and run at your own risk.

Update your environment with your api key:
```markdown
export OPENAI_API_KEY='[your key here]'
```

If a key isn't present in the environment then ChatTDD will prompt you to enter it.


## Usage

Once installed, you can use the chattdd command to interact with the tool. Here's how to use ChatTDD:

### Select a Model
You can choose between three models: text-davinci-003, gpt-3.5-turbo, and gpt-4. 
To select a model, use the following command:

```markdown
chattdd model text-davinci-003
```

Your model selection will be remembered for future sessions.

### Output Folder

```markdown
chattdd outputfolder [folder_path]
```
Sets the root folder for generated files. If this is left blank, files will be saved in the specified relative paths without a leading folder.

### Generate Test code & feature functions

Simply run
```markdown
chattdd
```
ChatTDD will ask for your requirement.
Alternative:

```markdown
chattdd test-and-code "sort a list of objects alphabetically"
```

ChatTDD will create the necessary Python files under the default directory or the directory you have setup with the 'outputfolder' command.

### Generate Only Test Code

```markdown
chattdd test "sort a list of objects alphabetically"
```

ChatTDD will create the necessary Python files under the `tests` directory.

## Contributing

If you'd like to contribute to the development of ChatTDD, please feel free to fork the repository and submit a pull request.

## License

ChatTDD is licensed under the MIT License. See the `LICENSE` file for more details.


