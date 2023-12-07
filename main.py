from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import Screen
from kivymd.uix.spinner import MDSpinner
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
            MDSpinner(
                size_hint=(None, None),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                active=True,
            )
        ]
        
        self.button_idx = 0
        self.current_button = self.buttons[self.button_idx]

        for idx in range(2):
            self.buttons[idx].bind(on_press=self.clickHandler)

        self.screen.add_widget(self.current_button)
        return self.screen
    
    def clickHandler(self, instance=None, do_nothing=False):
        recorder_thread = threading.Thread(target=self.toggleRecording, args=(do_nothing,))
        recorder_thread.start()
        self.threads.append(recorder_thread)
        self.screen.remove_widget(self.current_button)
        self.button_idx = (self.button_idx + 1) % 2
        print(self.button_idx)
        self.current_button = self.buttons[self.button_idx]
        self.screen.add_widget(self.current_button)

    # def joinThreads(self):
    #     # Join the threads when button_idx is 2
    #     for thread in self.threads:
    #         thread.join()
    #     self.threads = []
    #     self.clickHandler(do_nothing=True)


    def toggleRecording(self, do_nothing=False):
        if not do_nothing:
            if self.recording:
                self.recording = False
                print("Stop Recording...")
                # if self.button_idx == 2:
                #     # Schedule joining threads on the main thread
                #     Clock.schedule_once(lambda dt: self.joinThreads(), 0)
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
                self.recognizer.adjust_for_ambient_noise(source)
                while self.recording:
                    try:
                        idx += 1
                        audio = self.recognizer.listen(source, 5, 3)
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
    client_app = ClientApp()
    VoicChatGPTApp(client_app).run()
