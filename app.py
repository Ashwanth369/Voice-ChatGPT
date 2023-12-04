from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import Screen

class DemoApp(MDApp):
    def build(self):
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

    #this method is triggered when the button is clicked
    def change_button(self, instance):
        self.screen.remove_widget(self.current_button)
        self.button_idx = 1 - self.button_idx
        self.current_button = self.buttons[self.button_idx]
        self.screen.add_widget(self.current_button)

if __name__ == "__main__":
    DemoApp().run()