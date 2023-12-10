from kivy.app import App
from kivy.uix.label import Label
from bs4 import BeautifulSoup
import requests

class MyApp(App):
    def build(self):
        # Делаем запрос к веб-сайту
        url = 'https://example.com'
        response = requests.get(url)
        html_content = response.text

        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string

        # Создаем Kivy виджет
        label = Label(text=f'Title from BeautifulSoup: {title}')
        return label


if __name__ == '__main__':
    MyApp().run()