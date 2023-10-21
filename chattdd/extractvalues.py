from chattdd.tools import strip_extra_quotes
import re
import ast

def extract_value(s, key):
    # Try parsing as a dictionary
    try:
        dict_data = ast.literal_eval(s.strip())
        if isinstance(dict_data, dict):
            return dict_data.get(key)
    except (ValueError, SyntaxError):
        pass

    # If not a dictionary, interpret as the first format
    pattern = r"(?s){}\s*?:\s*(.*?)(?=\w+\s*:|$)".format(key)
    match = re.search(pattern, s)
    
    if match:
        stripped_string = strip_extra_quotes(match.group(1).strip())
        return stripped_string
    
    #Not found? That shouldn't be the case. 
    print(f'\nNew string format for a test\n{s}\n\n')
    raise ValueError(f"Could not extract value for key '{key}' from string.")

# Test cases
def test_extract_from_regular_format():
    s = "\n\ntest_code:\nimport pytest\n\ndef test_hello_world():\n    assert 'HELLO WORLD' == hello_world()\n\ndef hello_world():\n    return 'HELLO WORLD'\n\ncomment: This test checks that the hello_world() function returns the string 'HELLO WORLD' in capital letters."
    assert extract_value(s, 'test_code').startswith("import pytest")
    assert extract_value(s, 'comment') == "This test checks that the hello_world() function returns the string 'HELLO WORLD' in capital letters."

def test_extract_from_dict_format():
    s = "\n{\n    'test_code': 'import pytest\\n\\ndef test_sort_list_alphabetically():\\n    list_to_sort = [\\'z\\', \\'a\\', \\'b\\', \\'c\\']\\n    sorted_list = sorted(list_to_sort)\\n    assert sorted_list == [\\'a\\', \\'b\\', \\'c\\', \\'z\\']',\n    'comment': 'This test checks that the list is sorted alphabetically.'\n}"
    assert extract_value(s, 'test_code').startswith("import pytest")
    assert extract_value(s, 'comment') == "This test checks that the list is sorted alphabetically."

def test_another_extract_from_dict_format():
    s = '\n{\n    \'test_code\': \'import pytest\\n\\ndef test_hello_world():\\n    assert \'HELLO WORLD\' == hello_world(), "The output should be \'HELLO WORLD\'"\',\n    \'comment\': \'This test checks that the function hello_world() prints the words "HELLO WORLD" in capital letters.\'\n}'
    assert extract_value(s, 'test_code').startswith("import pytest")
    assert extract_value(s, 'comment') == 'This test checks that the function hello_world() prints the words "HELLO WORLD" in capital letters.'


def test_invalid_key():
    s = "\n{\n    'test_code': 'import pytest\\n\\ndef test_sort_list_alphabetically():\\n    list_to_sort = [\\'z\\', \\'a\\', \\'b\\', \\'c\\']\\n    sorted_list = sorted(list_to_sort)\\n    assert sorted_list == [\\'a\\', \\'b\\', \\'c\\', \\'z\\']',\n    'comment': 'This test checks that the list is sorted alphabetically.'\n}"
    assert extract_value(s, 'nonexistent_key') is None

def test_extract_from_dict_format2():
    s = '{\n"test_code": """\n# /path/to/test_word_occurrences.py\nimport pytest\nfrom word_occurrences import count_word_occurrences\n\ndef test_count_word_occurrences():\n    assert count_word_occurrences("Hello world") == {"Hello": 1, "world": 1}\n    assert count_word_occurrences("Hello Hello world") == {"Hello": 2, "world": 1}\n    assert count_word_occurrences("Hello world world world") == {"Hello": 1, "world": 3}\n    assert count_word_occurrences("") == {}\n    assert count_word_occurrences("Hello") == {"Hello": 1}\n\n@pytest.mark.parametrize("input_str, expected_output", [\n    ("Hello world", {"Hello": 1, "world": 1}),\n    ("Hello Hello world", {"Hello": 2, "world": 1}),\n    ("Hello world world world", {"Hello": 1, "world": 3}),\n    ("", {}),\n    ("Hello", {"Hello": 1}),\n])\ndef test_count_word_occurrences_with_parametrize(input_str, expected_output):\n    assert count_word_occurrences(input_str) == expected_output\n""",\n"comment": "The tests cover different scenarios including multiple occurrences of the same word, no occurrences (empty string), and a single occurrence of a word. The second test function uses pytest\'s parametrize feature to run the same test with different inputs and expected outputs."\n}'
    assert extract_value(s, 'test_code').startswith("# /path/to/test_word_occurrences.py")

def test_strangethings():
    s = "\n        code_word: 'OK'\n        test_code:\nimport pytest\nimport random\n\ndef is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, n):\n        if n % i == 0:\n            return False\n    return True\n\ndef test_is_prime():\n    assert is_prime(2) == True\n    assert is_prime(3) == True\n    assert is_prime(4) == False\n    assert is_prime(5) == True\n    assert is_prime(6) == False\n\ndef random_prime():\n    while True:\n        n = random.randint(100, 1000)\n        if is_prime(n):\n            return n\n\ndef test_random_prime():\n    for _ in range(100):\n        n = random_prime()\n        assert n >= 100 and n <= 1000\n        assert is_prime(n)\n\ncomment: The tests cover the requirements of returning a random prime number between 100 and 1000."
    assert extract_value(s, 'test_code').startswith("import pytest")