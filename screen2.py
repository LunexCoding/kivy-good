from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from schedule import g_scheduleParser


class Screen2(Screen):
    def __init__(self, **kwargs):
        super(Screen2, self).__init__(**kwargs)
        layout = GridLayout(cols=3)
        layout.add_widget(Button(text='Switch to Screen 1', on_press=self.switch_screen))
        for group in g_scheduleParser.groups:
            label = Label(text=group)
            layout.add_widget(label)
        self.add_widget(layout)


    def switch_screen(self, instance):
        self.manager.current = 'screen1'
