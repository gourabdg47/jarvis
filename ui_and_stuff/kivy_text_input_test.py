import kivy
#kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

Window.size = (400,130)

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class LblTxt(BoxLayout):
    
    theTxt = ObjectProperty(None)

class MyApp(App):

    def build(self):
        self.root = Builder.load_file('simpleForm.kv')
        
        return self.root


if __name__ == '__main__':
    MyApp().run()

# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.lang import Builder


# Builder.load_file('simpleForm.kv')


# class UI(Widget):
#     pass


# class UIApp(App):
#     def build(self):
#         return UI()

#     def process(self):
#         text = self.root.ids.input.text
#         print(text)


# if __name__ == "__main__":
#     UIApp().run()