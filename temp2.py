from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
import asyncio, time
import threading
import time

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDRaisedButton:
        text: 'Click me'
        on_release: app.async_operation_trigger()
'''

class MyApp(MDApp):
    def build(self):
        self.event_loop = asyncio.get_event_loop()
        return Builder.load_string(KV)

    def update_ui(self, result):
        print(f'Async operation result: {result}')

    def async_function(self):
        time.sleep(3)  # Simulate an asynchronous task
        result = "Async function completed"
        self.update_ui(result)

    def async_operation_trigger(self):
        print("Clicked ME")
        # Start the asynchronous operation in a separate thread
        threading.Thread(target=self.async_function).start()

if __name__ == '__main__':
    MyApp().run()