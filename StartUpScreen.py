from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


class StartUp(MDScreen):
    """ Displays the app logo for 2 seconds upon startup of the program """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        img = Image(source='logo.png')
        self.add_widget(img)
        Clock.schedule_once(self.on_leave, 2)

    def on_leave(self, *args):
        self.clear_widgets()
        self.manager.current = 'MainScreen'
