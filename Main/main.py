import sys

import chatGPT as GPT
import voice_module as vm
import natural_language_processing as nlplib

if len(sys.argv) < 2:
    raise ValueError('Insufficient Arguments - You should enter the API Key')

API_key = sys.argv[1]

chatGPT = GPT.ChatGPT(API_key=API_key)
voiceModule = vm.VoiceModule(speaker=5810)
nlp = nlplib.NaturalLanguageProcessing(model="en_core_web_md")

commands = [
    {"text": "enter in local mode operation", "action": "local_mode"},
    {"text": "local mode operation", "action": "local_mode"},
    {"text": "use local files", "action": "local_mode"},
    {"text": "run local scripts", "action": "local_mode"},
    {"text": "access internal files", "action": "local_mode"},
    {"text": "ask ChatGPT for help", "action": "ChatGPT"},
    {"text": "use ChatGPT", "action": "ChatGPT"},
    {"text": "ChatGPT", "action": "ChatGPT"},
    {"text": "end conversation", "action": "exit"},
    {"text": "exit", "action": "exit"}
]

while True:
    operation_mode = nlp.choose_right_command(commands=commands, chatGPT=chatGPT, voiceModule=voiceModule)

    match operation_mode:
        case "local_mode":
            print("local mode")

        case "ChatGPT":
            print("ChatGPT")

            message = input("Ask ChatGPT: ")
            response = chatGPT.conversation(message=message, nlp=nlp)

            while response != "":
                voiceModule.speak(response)
                message = input("Ask ChatGPT: ")
                response = chatGPT.conversation(message=message, nlp=nlp)

        case "exit":
            print("exit")
            sys.exit(0)
