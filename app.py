from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screen1 import Screen1
from screen2 import Screen2


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Screen1(name='screen1'))
        sm.add_widget(Screen2(name='screen2'))
        return sm
