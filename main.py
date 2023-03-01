from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from AddHabitScreen import AddHabit
from EditScreen import EditScreen
from MainScreen import MainScreen
from StartUpScreen import StartUp
from MetricsScreen import MetricsScreen


class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        # Initialize screen manager
        sm = MDScreenManager()
        # List screens
        sm.add_widget(StartUp(name='Start Up'))
        sm.add_widget(MainScreen(name='MainScreen'))
        sm.add_widget(AddHabit(name='Add new habit'))
        sm.add_widget(EditScreen(name='EditScreen'))
        sm.add_widget(MetricsScreen(name='MetricsScreen'))
        # Set window name
        self.title = 'Habit Tracker'

        return sm


# run the app
if __name__ == "__main__":
    MainApp().run()
