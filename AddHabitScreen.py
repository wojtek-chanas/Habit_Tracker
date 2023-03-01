from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from functions import habits, add_habit, positive_int_input_filter
from data import save_changes


class AddHabit(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):

        # name variable with required parameter set to True
        name = MDTextField(hint_text='Habit Name', text='Sample name', helper_text='Name is required!',
                           helper_text_mode='on_error', font_size=28, size_hint_y=None, height=50,
                           pos_hint={'center_x': 0.5, 'center_y': 0.9}, required=True, error_color=(1, 0, 0, 1))

        # adding description is optional
        description = MDTextField(hint_text='Habit description',
                                  helper_text='Elaborate a bit more, specify what\'s __init__ ;)',
                                  helper_text_mode='on_focus', font_size=24, size_hint_y=None, height=50,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.7})

        goal = MDTextField(hint_text='Goal',
                           text='15',
                           helper_text='The goal must be an integer larger than 0',
                           helper_text_mode='on_error',
                           required=True,
                           error_color=(1, 0, 0, 1),
                           font_size=24,
                           size_hint_y=None,
                           height=50,
                           pos_hint={'center_x': 0.5, 'center_y': 0.5},
                           input_filter=positive_int_input_filter)

        # Frequency displays an options list, to prevent user's typos from causing errors
        frequency = Spinner(values=("Days", "Weeks", "Months"), font_size=24, size_hint_y=None, height=50,
                            pos_hint={'center_x': 0.5, 'center_y': 0.35},
                            text='Select habit\'s frequency')

        # Create buttons
        save_button = Button(text='Save', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.4, 'center_y': 0.1})
        cancel_button = Button(text='Cancel', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.6, 'center_y': 0.1})

        # Bind buttons to functions
        save_button.bind(on_release=lambda x: self.save(name.text, description.text, goal.text, frequency.text))
        cancel_button.bind(on_release=self.cancel)

        # Add everything to the screen
        self.add_widget(frequency)
        self.add_widget(name)
        self.add_widget(description)
        self.add_widget(goal)
        self.add_widget(save_button)
        self.add_widget(cancel_button)

    def save(self, name, description, goal, frequency):
        """ Function passes parameters to add_habit() function, brings user back to the MainScreen and refreshes
         the data table on the MainScreen if all the parameters are correct. If one or more required parameters
         are wrong the function won't do anything """
        if not name == "" and not goal == "" and frequency in ("Days", "Weeks", "Months"):
            add_habit(name, description, goal, frequency)
            self.manager.current = 'MainScreen'
            self.manager.get_screen("MainScreen").table.row_data = [(habit.index + 1, habit.name, habit.description,
                                                                    habit.when_done(), habit.count_streak()) for habit
                                                                    in habits]
            save_changes(habits)
            self.manager.current = 'MainScreen'
        else:
            pass

    def cancel(self, *args):
        self.manager.current = 'MainScreen'

    def on_leave(self, *args):
        self.clear_widgets()

