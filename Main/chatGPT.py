import openai

class ChatGPT:
    def __init__(self, API_key, max_tokens = 500):
        openai.api_key = API_key
        self._conversation = [{"role": "system", "content": "You are a helpful assistant"}]
        self._rephrase = []
        self.used_tokens = 0
        self.max_tokens = max_tokens


    def rephrase(self, message):
        self._rephrase = [
            {"role": "system", "content": "You are a helpful assistant that rephrases given sentances"},
            {"role": "user", "content": "Rephrase this sentance: " + message}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=self._rephrase, 
            max_tokens=self.max_tokens
        )

        assistant_reply = response.choices[0].message['content']
        print("Assistant's Reply: " + assistant_reply)

        total_tokens = response.usage['total_tokens']
        print('Used tokens: ' + str(total_tokens))

        return assistant_reply
    

    def conversation(self, message, max_history_len = 21):
        if len(self._conversation) > max_history_len:
            self._conversation = list(self._conversation[0]).append(self._conversation[3:])

        self._conversation.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._conversation, 
            max_tokens=self.max_tokens
            
        )

        assistant_reply = response.choices[0].message['content']
        print("Assistant's Reply: " + assistant_reply)

        self._conversation.append({"role": "assistant", "content": assistant_reply})

        total_tokens = response.usage['total_tokens']
        self.used_tokens = self.used_tokens + total_tokens

        print('Total message tokens: ' + str(total_tokens))
        print('Used tokens: ' + str(self.used_tokens))


        return assistant_reply
    

    def clear_conversation_history(self):
        self._conversation = [{"role": "system", "content": "You are a helpful assistant"}]
        self.used_tokens = 0


# uncomment for test


# message = input("Enter your message: ")
# chat.conversation(message)

# message = input("Enter your message: ")
# chat.conversation(message)

# message = input("Enter your message: ")
# chat.conversation(message)

# print('\n\n\n\n')
# print(chat._conversation)