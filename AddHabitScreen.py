from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from functions import habits, add_habit, positive_int_input_filter
from data import save_changes


class AddHabit(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name_err = None
        self.goal_err = None
        self.frequency_err = None

    def on_enter(self, *args):

        # name variable with required parameter set to True
        name = MDTextField(hint_text='Habit Name', max_text_length=16,
                           text='Sample Habit',
                           helper_text='Name is required!',
                           helper_text_mode='on_error',
                           font_size=28,
                           size_hint_y=None,
                           height=50,
                           pos_hint={'center_x': 0.5, 'center_y': 0.9},
                           required=True,
                           error_color=(1, 0, 0, 1))

        # adding description is optional
        description = MDTextField(hint_text='Habit description',
                                  helper_text='Elaborate a bit more, specify what\'s __init__ ;)',
                                  helper_text_mode='on_focus',
                                  font_size=24,
                                  size_hint_y=None,
                                  height=50,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.7})

        goal = MDTextField(hint_text='Goal',
                           max_text_length=5,
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
        frequency = Spinner(values=("Days", "Weeks", "Months"),
                            font_size=24,
                            size_hint_y=None,
                            height=50,
                            pos_hint={'center_x': 0.5, 'center_y': 0.35},
                            text='Select habit\'s periodicity')

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
        """ Function passes parameters to add_habit() function and brings user back to the MainScreen if all the
         parameters are correct. Otherwise, it displays an error message. """
        while len(goal) > 1 and goal[0] == '0':  # Remove excessive zeros from the input, eg. 007 --> 7
            goal = goal[1:]
        if goal == "0":
            if self.goal_err is not None:
                self.remove_widget(self.goal_err)
            self.goal_err = MDLabel(text='Goal cannot be zero!',
                                    halign='left',
                                    font_size=24,
                                    size_hint=(0.25, 0.9),
                                    height=50,
                                    theme_text_color='Error',
                                    pos_hint={'center_x': 0.13, 'center_y': 0.43},
                                    text_color=(1, 0, 0, 1))
            self.add_widget(self.goal_err)
            Clock.schedule_once(lambda x: self.remove_widget(self.goal_err), 3)

        if name in [habit.name for habit in habits]:
            if self.name_err is not None:
                # Prevents error message from getting stuck on the screen if called more than once
                self.remove_widget(self.name_err)
            self.name_err = MDLabel(text='Name already exists!',
                                    halign='left',
                                    font_size=24, size_hint=(0.25, 0.9),
                                    height=50, theme_text_color='Error',
                                    pos_hint={'center_x': 0.13, 'center_y': 0.83},
                                    text_color=(1, 0, 0, 1))
            self.add_widget(self.name_err)
            Clock.schedule_once(lambda x: self.remove_widget(self.name_err), 3)

        elif not name == "" and not goal == "" and frequency in ("Days", "Weeks", "Months"):
            add_habit(name, description, goal, frequency)
            self.manager.current = 'MainScreen'
            self.manager.get_screen("MainScreen").table.row_data = [(habit.index + 1, habit.name, habit.description,
                                                                    habit.when_done(), habit.count_streak()) for habit
                                                                    in habits]
            save_changes(habits)
            self.manager.current = 'MainScreen'
            
        elif frequency not in ("Days", "Weeks", "Months"):
            if self.frequency_err is not None:
                self.remove_widget(self.frequency_err)
            self.frequency_err = MDLabel(text='Select the periodicity first!', halign='center',
                                         font_size=24, size_hint=(0.25, 0.9), height=50, theme_text_color='Error',
                                         pos_hint={'center_x': 0.5, 'center_y': 0.2}, text_color=(1, 0, 0, 1))
            self.add_widget(self.frequency_err)
            Clock.schedule_once(lambda x: self.remove_widget(self.frequency_err), 2)

        else:
            pass

    def cancel(self, *args):
        self.manager.current = 'MainScreen'

    def on_leave(self, *args):
        self.clear_widgets()
