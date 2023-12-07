from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.spinner import MDSpinner
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading
import time

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "50"
        self.theme_cls.theme_style = "Dark"
        
        self.screen = Screen()
        layout = BoxLayout(orientation='vertical')
        
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

        # Add buttons to the layout
        self.current_button_index = 0
        
        for button in self.buttons:
            layout.add_widget(button)
            if isinstance(button, MDFloatingActionButton):
                button.bind(on_release=self.run_threads)

        # Add the spinner to the layout
        self.spinner = MDSpinner(
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "y": 0.1},
            active=False,
        )
        layout.add_widget(self.spinner)

        self.screen.add_widget(layout)
        return self.screen

    def run_threads(self, *args):
        # Deactivate the spinner (if it's active)
        self.spinner.active = False

        # Toggle between the two buttons
        self.current_button_index = (self.current_button_index + 1) % 2
        current_button = self.buttons[self.current_button_index]

        # Activate the spinner
        self.spinner.active = True
        thread = threading.Thread(target=self.run_threads_function)
        thread.start()

    def run_threads_function(self):
        time.sleep(5)
        Clock.schedule_once(self.deactivate_spinner, 0)

    def deactivate_spinner(self, dt):
        # Deactivate the spinner
        self.spinner.active = False

MyApp().run()
