from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import Screen
from kivy.clock import Clock
from textToSpeech import textToSpeech
import speech_recognition as sr
import threading
from client import ClientApp
from vosk import Model, KaldiRecognizer

class VoicChatGPTApp(MDApp):

    def __init__(self, client_app, **kwargs):
        super().__init__(**kwargs)
        self.client_app = client_app

    def build(self):
        self.model = Model("vosk-model-small-en-us-0.15")
        self.recognizer  = KaldiRecognizer(self.model, 16000)

        self.recording = False
        self.results = [""]*100

        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "50"
        self.theme_cls.theme_style = "Dark"
        
        self.screen = Screen()
        
        self.buttons = [
            MDFloatingActionButton(icon="microphone",
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                    theme_icon_color="Custom",
                                    md_bg_color="#e9dff7",
                                    icon_color="#6851a5"),
            MDFloatingActionButton(icon="record",
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                   theme_icon_color="Custom",
                                   md_bg_color="#e9dff7",
                                   icon_color="#6851a5")
        ]
        
        self.button_idx = 0
        self.current_button = self.buttons[self.button_idx]

        for button in self.buttons:
            button.bind(on_press=self.clickHandler)

        self.screen.add_widget(self.current_button)

        

        return self.screen
    
    def clickHandler(self, instance=None):
        threading.Thread(target=self.toggleRecording).start()
        self.screen.remove_widget(self.current_button)
        self.button_idx = 1 - self.button_idx
        self.current_button = self.buttons[self.button_idx]
        self.screen.add_widget(self.current_button)

    def toggleRecording(self):
        if self.recording:
            self.recording = False
            print("Stop Recording...")
        else:
            self.recording = True
            print("Start Recording...")
            threading.Thread(target=self.record).start()

    def record(self):
        while self.recording:
            idx = 0
            tasks = list()
            self.results = [""]*100
            with self.microphone as source:
                while self.recording:
                    try:
                        audio = source.read(1024)
                        task = threading.Thread(target=self.speechToText, args=(audio,idx,), daemon=True)
                        # print(idx,task)
                        tasks.append(task)
                        task.start()
                    except Exception:
                        continue

        for task in tasks:
            task.join()

        text = None
        for res in self.results:
            if res is not None and len(res) > 0:
                if text is None:
                    text = res
                else:
                    text += " " + res
        print("Resulting text to speech:", text)

        if(text is None):
            textToSpeech("Please provide some input. The input cannot be empty!")
        else:
            chatGPTResponse = self.client_app.sendMessage(text)
            textToSpeech(chatGPTResponse)
        
        del self.results[:]
        

    def speechToText(self, audio, idx):
        text = ""
        try:
            text = self.recognizer.AcceptWaveform(audio)
        except Exception as e:
            print(f"An error occurred: {e}")

        self.results[idx] = text
        return text
    
if __name__ == "__main__":
    # flag = True
    client_app = ClientApp()
    VoicChatGPTApp(client_app).run()
