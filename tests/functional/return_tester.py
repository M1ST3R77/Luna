import os
import sys
import json
import subprocess

def find_best_intent(db_data, input):
    """
    Find the best matching intent based on the given input.

    :param dict db_data: The database containing intents and their patterns.
    :param str input: The user input to match against patterns.
    :return: The best matching intent or the "non_reconnu" intent if no match is found.
    :rtype: dict
    """
    input_words = set(input.lower().split())
    best = None
    max = 0

    for intent in db_data["intents"]:
        matches = 0
        for pattern in intent["patterns"]:
            pattern_words = set(pattern.lower().split())
            matches = len(input_words & pattern_words) + matches
            if matches > max:
                max = matches
                best = intent
    if best is None:
        for intent in db_data["intents"]:
            if intent["tag"] == "non_reconnu":
                return intent
    return best

def check_db(db_data, ai_response):
    """
    Check if the AI response exists in the database.

    :param dict db_data: The database containing intents and responses.
    :param str ai_response: The AI response to check.
    :return: True if the response exists in the database, False otherwise.
    :rtype: bool
    """
    for intent in db_data["intents"]:
        if ai_response in intent["responses"]:
            return True
    return False

def return_tester(executable_path, test_file, debug=False):
    """
    Test the AI chatbot's responses against expected database responses.

    :param str executable_path: The path to the chatbot executable.
    :param str test_file: The file containing test inputs.
    :param bool debug: Whether to run the chatbot in debug mode, defaults to False.
    :return: 0 if all responses are correct, 1 if an error occurs.
    :rtype: int
    """
    db_file = "./src/db.json"
    expected_responses = {}

    if not os.path.exists(db_file):
        print(f"Database file {db_file} not found.", file=sys.stderr)
        return 1

    with open(db_file, 'r', encoding='utf-8') as file:
        db_data = json.load(file)

    for intent in db_data["intents"]:
        for pattern in intent["patterns"]:
            expected_responses[pattern.lower()] = intent["responses"]

    command = [executable_path, test_file]

    if debug:
        command.append("-d")

    try:
        result = subprocess.run(command, capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {executable_path}: {e}", file=sys.stderr)
        return 1
    
    print(result.stdout, end="")

    output_lines = result.stdout.splitlines()
    with open(test_file, 'r', encoding='utf-8') as file:
        test_inputs = [line.strip() for line in file if line.strip()]
    
    user_index = 0
    for ai_response in output_lines:
        if not check_db(db_data, ai_response):
            continue
        expected = find_best_intent(db_data, test_inputs[user_index])["responses"]
        if ai_response in expected:
            print(f"Correct answer for '{test_inputs[user_index]}': '{ai_response}'")
            user_index += 1
        else:
            print(f"Incorrect answer for '{test_inputs[user_index]}': '{ai_response}'. Expected : {expected}", file=sys.stderr)
            return 1

    return 0
