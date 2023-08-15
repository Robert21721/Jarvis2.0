import spacy

# Load the spaCy English NLP model
nlp = spacy.load("en_core_web_md")

# List of predefined commands
commands = [
    {"text": "open file", "action": "open_file"},
    {"text": "google search", "action": "search_internet"},
    # Add more commands as needed
]

def compare_commands(user_input):
    # Preprocess user input
    doc = nlp(user_input)
    user_tokens = [token.text for token in doc if not token.is_stop]

    # Compare user input with each command
    best_match = None
    highest_similarity = 0.0

    for command in commands:
        command_text = command["text"]
        command_doc = nlp(command_text)
        similarity = doc.similarity(command_doc)

        if similarity > highest_similarity:
            best_match = command
            highest_similarity = similarity

    return (best_match, highest_similarity)

# User input
user_input = input("Enter a command: ")

best_matched_command, highest_similarity_command = compare_commands(user_input)


if best_matched_command:
    print("Best matched command:", best_matched_command["text"])
    # Perform the corresponding action based on best_matched_command["action"]
else:
    print("No matching command found.")

print(highest_similarity_command)