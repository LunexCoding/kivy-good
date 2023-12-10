from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button


class Screen1(Screen):
    def __init__(self, **kwargs):
        super(Screen1, self).__init__(**kwargs)
        self.add_widget(Button(text='Switch to Screen 2', on_press=self.switch_screen))

    def switch_screen(self, instance):
        self.manager.current = 'screen2'
