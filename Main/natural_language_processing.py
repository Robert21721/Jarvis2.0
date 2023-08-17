import spacy
import warnings

class NaturalLanguageProcessing:
    def __init__(self, model="en_core_web_md"):
        self.nlp = spacy.load(model)
    

    def _compare_commands(self, user_input, commands):
        # Preprocess user input
        doc = self.nlp(user_input)

        # Compare user input with each command
        best_match = None
        highest_similarity = 0.0

        for command in commands:
            command_text = command["text"]
            command_doc = self.nlp(command_text)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                similarity = doc.similarity(command_doc)

            if similarity > highest_similarity:
                best_match = command
                highest_similarity = similarity

        return (best_match, highest_similarity)
    
    def choose_right_command(self, commands, chatGPT, voiceModule, threshold = 0.5):
        while True:
            user_input = input("Your Command: ")

            chosen_command = self._compare_commands(user_input=user_input, commands=commands)

            if chosen_command[1] >= threshold:
                return chosen_command[0]["action"]
            
            else:
                text = chatGPT.rephrase("I am not sure what should I do next. Can you be more precise?")
                voiceModule.speak(text=text)

    def exit_check(self,user_input, exit_commands, threshold=0.6):
        chosen_command = self._compare_commands(user_input=user_input, commands=exit_commands)

        print(chosen_command)

        if chosen_command[1] < threshold:
            return False
        
        return True