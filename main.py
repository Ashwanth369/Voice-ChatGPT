
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import Screen
from kivymd.uix.spinner import MDSpinner
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from textToSpeech import textToSpeech
import speech_recognition as sr
import threading
from client import ClientApp

class VoicChatGPTApp(MDApp):

    def __init__(self, client_app, **kwargs):
        super().__init__(**kwargs)
        self.client_app = client_app

    def build(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recording = False
        self.results = [""]*100
        self.threads = []

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
                                   icon_color="#6851a5"),
        ]

        self.spinner = MDSpinner(
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "y": 0.1},
            active=False,
        )
        
        self.button_idx = 0
        self.current_button = self.buttons[self.button_idx]

        for idx in range(2):
            self.buttons[idx].bind(on_press=self.clickHandler)

        self.screen.add_widget(self.current_button)
        self.screen.add_widget(self.spinner)
        return self.screen
    
    def clickHandler(self, instance=None):
        threading.Thread(target=self.toggleRecording).start()
        if self.button_idx == 1:
            self.screen.remove_widget(self.buttons[1])
            self.button_idx = 0
            self.spinner.active = True
            threading.Thread(target=self.processRecording).start()
        else:
            self.screen.remove_widget(self.buttons[0])
            self.button_idx = 1
            self.screen.add_widget(self.buttons[1])

    def processRecording(self):
        for thread in self.threads:
            thread.join()
        self.threads = []
        Clock.schedule_once(self.deactivate_spinner, 0)

    def deactivate_spinner(self, dt):
        self.spinner.active = False
        self.screen.add_widget(self.buttons[0])

    def toggleRecording(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            thread = threading.Thread(target=self.record)
            thread.start()
            self.threads.append(thread)

    def record(self):
        while self.recording:
            idx = 0
            tasks = list()
            self.results = [""]*100
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while self.recording:
                    try:
                        idx += 1
                        audio = self.recognizer.listen(source, 5, 4)
                        task = threading.Thread(target=self.speechToText, args=(audio,idx,), daemon=True)
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

        if text is None :
            textToSpeech("Sorry! I couldn't understand that.")
        else:
            chatGPTResponse = self.client_app.sendMessage(text)
            textToSpeech(chatGPTResponse)
        
        del self.results[:]

    def speechToText(self, audio, idx):
        text = ""
        try:
            text = self.recognizer.recognize_google(audio)
        except Exception as e:
            print(f"An error occurred: {e}")

        self.results[idx] = text
        return text
    
if __name__ == "__main__":
    client_app = ClientApp(host="3.17.4.67", port=12345)
    VoicChatGPTApp(client_app).run()
