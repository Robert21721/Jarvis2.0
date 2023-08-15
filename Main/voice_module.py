from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from playsound import playsound
import os

class VoiceModule:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(self.device)
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(self.device)
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.output_filename = '../AudioFiles/response.mp3'


    def create_audio_file(self, text, speaker=5810):
        inputs = self.processor(text=text, return_tensors="pt").to(self.device)
        speaker_embeddings = torch.tensor(self.embeddings_dataset[speaker]["xvector"]).unsqueeze(0).to(self.device)
        speech = self.model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=self.vocoder)
        sf.write(self.output_filename, speech.cpu().numpy(), samplerate=16000)

    def delete_audio_file(self):
        os.remove(self.output_filename)

    def play_audio_file(self):
        playsound(self.output_filename)

    def response(self, text, speaker=5810):
        self.create_audio_file(text=text, speaker=speaker)
        self.play_audio_file()
        self.delete_audio_file()


# uncomment for testing
####################################################

# text = """Allow me to introduce myself: I am Jarvis, 
#     the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can:
#     twenty four hours a day, seven days a week. """

# voice = VoiceModule()
# voice.response(text)
 