
# ChatTDD

ChatTDD is a Python utility designed to assist developers in building Test-Driven Python code. By leveraging the OpenAI API, ChatTDD automates the generation of function code and corresponding tests based on a simple textual description of the desired functionality.

## Installation

To install ChatTDD, ensure you have Python 3.9 installed, then run the following command:

```markdown
pip install ChatTDD
```

## Configuration

Before using ChatTDD, you'll need to have an OpenAI API key. If you don't have one, you can obtain it from [OpenAI](https://beta.openai.com/signup/).

On the first run, ChatTDD will prompt you to enter your OpenAI API key, which will be saved for future use.

## Usage

ChatTDD provides two main commands: `test-and-code` and `test`. 

- The `test-and-code` command generates both the function code and the test code based on the provided description.
- The `test` command generates only the test code.

Here's how you can use these commands:

### Generate Function and Test Code

```markdown
chattdd test-and-code "sort a list of objects alphabetically"
```

### Generate Only Test Code

```markdown
chattdd test "sort a list of objects alphabetically"
```

ChatTDD will create the necessary Python files under the `src` and `tests` directories respectively.

## Contributing

If you'd like to contribute to the development of ChatTDD, please feel free to fork the repository and submit a pull request.

## License

ChatTDD is licensed under the MIT License. See the `LICENSE` file for more details.


