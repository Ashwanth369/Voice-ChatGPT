from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import Screen
from kivy.clock import Clock
import time

import asyncio
import speech_recognition as sr
import aioconsole

class DemoApp(MDApp):

    def build(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.flag = True
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
            button.bind(on_press=self.change_button)

        self.screen.add_widget(self.current_button)

        return self.screen

    def change_button(self, instance):
        if instance == self.buttons[0]:  # Microphone button
            self.start_listening()
        else:  # Record button
            self.stop_listening()

    def start_listening(self):
        print("StartL")
        self.screen.remove_widget(self.current_button)
        self.button_idx = 1
        self.current_button = self.buttons[self.button_idx]
        self.screen.add_widget(self.current_button)
        
        Clock.schedule_interval(self.listen_and_update, 0.1)
        #time.sleep(10)
        print("Bye2!")

    def stop_listening(self):
        print("StopL")
        self.screen.remove_widget(self.current_button)
        # self.button_idx = 0
        # self.current_button = self.buttons[self.button_idx]
        # self.screen.add_widget(self.current_button)
        #Clock.unschedule(self.listen_and_update)
        #global flag
        self.flag = False

    def listen_and_update(self, dt):
        print("Hello")
        asyncio.run(self.update_text())
        print("Bye!")

    async def update_text(self):
        print("update_text method")
        text = await self.main2()
        print("Partial Result:", " ".join([r for r in text if len(r) > 0]))

    async def f1(self, audio):
        text = ""
        try:
            text = self.recognizer.recognize_google(audio)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")
        return text

    async def user_input(self):
        if self.flag:
        #await aioconsole.ainput("Press Enter to stop recording:")
        print("ui")
        time.sleep(5)
        print("ui_end")
        self.flag = False

    async def f2(self):
        tasks = []
        i = 0
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

            while self.flag:
                try:
                    print(i, self.flag)
                    i += 1
                    audio = await asyncio.to_thread(self.recognizer.listen, source, 5, 2)
                    task = asyncio.create_task(self.f1(audio))
                    tasks.append(task)
                except Exception:
                    continue

        print(self.flag)
        results = await asyncio.gather(*tasks)
        print("End of f2")
        return results

    async def main2(self):
        results, _ = await asyncio.gather(self.f2(), self.user_input())
        text = []
        for res in results:
            if res is not None and len(res) > 0:
                text.append(res)
        print("End of main2")
        return text

if __name__ == "__main__":
    # flag = True
    DemoApp().run()
