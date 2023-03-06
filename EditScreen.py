from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from functions import habits, positive_int_input_filter
from data import save_changes


def fetch_index():
    """ Returns the current index of selected habit """
    from MainScreen import current_habit_index as chi
    temp_var = chi
    return temp_var


class EditScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name_err = None
        self.error_message = None
        self.err_message_box = None
        self.goal_err = None
        self.frequency = None
        self.habit_name = None
        self.description = None
        self.goal = None
        self.dialog = None

        save_button = Button(text='Save changes', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.4, 'center_y': 0.2})
        save_button.bind(on_release=self.save)
        self.add_widget(save_button)

        cancel_button = Button(text='Cancel', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.6, 'center_y': 0.2})
        cancel_button.bind(on_release=self.cancel)
        self.add_widget(cancel_button)

        delete_button = Button(text='Delete Habit', size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        delete_button.bind(on_release=self.confirm_dbox)
        self.add_widget(delete_button)

    def on_enter(self, *args):
        print('current index= ', fetch_index())
        try:
            self.habit_name = MDTextField(hint_text='Change habit name',
                                          text=habits[fetch_index()].name,
                                          mode="fill",
                                          helper_text='Name can\'t be empty.',
                                          required=True,
                                          max_text_length=16,
                                          helper_text_mode='on_error',
                                          font_size=24,
                                          size_hint=(0.9, None),
                                          height=50,
                                          pos_hint={'center_x': 0.5, 'center_y': 0.9})

            self.description = MDTextField(hint_text='Description',
                                           text=habits[fetch_index()].description,
                                           mode="fill",
                                           helper_text='Type in a new description.',
                                           helper_text_mode='on_focus',
                                           font_size=24, size_hint=(0.9, None),
                                           height=50,
                                           pos_hint={'center_x': 0.5, 'center_y': 0.7})

            self.goal = MDTextField(hint_text='Goal',
                                    text=habits[fetch_index()].goal,
                                    mode="fill",
                                    max_text_length=5,
                                    helper_text='The goal must be an integer larger than 0',
                                    required=True,
                                    helper_text_mode='on_error',
                                    font_size=24, size_hint=(0.9, None),
                                    height=50,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                    input_filter=positive_int_input_filter)

            self.frequency = Spinner(values=("Days", "Weeks", "Months"),
                                     font_size=24,
                                     size_hint_y=None,
                                     height=50,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.35},
                                     text=habits[fetch_index()].frequency)

            self.add_widget(self.habit_name)
            self.add_widget(self.description)
            self.add_widget(self.goal)
            self.add_widget(self.frequency)

        except IndexError:
            self.error_message = MDLabel(text=f"Nothing to see here... \nCome back later!",
                                         font_size=24,
                                         size_hint=(0.9, 0.9),
                                         height=50,
                                         halign='center',
                                         pos_hint={'center_x': 0.5, 'center_y': 0.5})

            self.err_message_box = MDBoxLayout(orientation='vertical',
                                               size_hint=(0.9, 0.1),
                                               pos_hint={'center_x': 0.5, 'center_y': 0.5})
            self.err_message_box.add_widget(self.error_message)
            self.add_widget(self.err_message_box)

    def confirm_dbox(self, *args):
        """ Displays dialog box to confirm habit deletion """
        try:
            delete_button = MDFlatButton(text='Delete', on_release=self.delete)
            cancel_button = MDFlatButton(text='Cancel', on_release=self.dbox_cancel)

            self.dialog = MDDialog(title='Delete Habit',
                                   text=f'Are you sure? Habit: {habits[fetch_index()].name} '
                                        f'and its data will be lost.',
                                   size_hint=(0.6, 0.2),
                                   buttons=[delete_button, cancel_button])
            self.dialog.open()

        except IndexError:
            pass

    def dbox_cancel(self, *args):
        self.dialog.dismiss()

    def delete(self, *args):
        """ Delete current habit from habits list """
        self.dialog.dismiss()
        del habits[fetch_index()]
        # Reassign Habit's class self.index values
        for habit in habits:
            print(f"Habit {habit.name} index was updated from {habit.index}")
            habit.index = habits.index(habit)
            print(f"to index = {habit.index}.")
        save_changes(habits)
        self.manager.current = 'MainScreen'

    def save(self, instance):
        """ Reassigns Habit object attributes name, description, goal and periodicity using TextField's values. """
        try:
            counter = 0
            for habit in habits:
                if self.habit_name.text == habit.name:
                    counter += 1
            if counter > 1:
                if self.name_err is not None:
                    # Prevents error message from getting stuck on the screen if called more than once
                    self.remove_widget(self.name_err)
                self.name_err = MDLabel(text='Name already exists!',
                                        font_size=24,
                                        size_hint=(0.25, 0.9),
                                        height=50,
                                        theme_text_color='Error',
                                        pos_hint={'center_x': 0.19, 'center_y': 0.83},
                                        text_color=(1, 0, 0, 1))
                self.add_widget(self.name_err)
                Clock.schedule_once(lambda x: self.remove_widget(self.name_err), 2)

            elif self.goal.text[0] == '0':  # Remove excessive zeros from the input, eg. 007 --> 7
                while len(self.goal.text) > 1 and self.goal.text[0] == '0':
                    self.goal.text = self.goal.text[1:]
                if self.goal.text == "0":
                    if self.goal_err is not None:
                        self.remove_widget(self.goal_err)
                    self.goal_err = MDLabel(text='Goal cannot be zero!',
                                            font_size=24,
                                            size_hint=(0.25, 0.9),
                                            height=50,
                                            theme_text_color='Error',
                                            pos_hint={'center_x': 0.19, 'center_y': 0.43},
                                            text_color=(1, 0, 0, 1))

                    self.add_widget(self.goal_err)
                    Clock.schedule_once(lambda x: self.remove_widget(self.goal_err), 3)
            elif not self.habit_name.text == "" and not self.goal.text == "" and not self.goal.text == '0':
                habits[fetch_index()].name = self.habit_name.text
                habits[fetch_index()].description = self.description.text
                habits[fetch_index()].goal = self.goal.text
                habits[fetch_index()].frequency = self.frequency.text
                save_changes(habits)
                print("Changes has been saved.")
                self.manager.current = 'MainScreen'

        except AttributeError:
            pass
        except IndexError:
            pass

    def on_leave(self, *args):
        """ Clears the text fields """
        try:
            self.remove_widget(self.habit_name)
            self.remove_widget(self.description)
            self.remove_widget(self.goal)
            self.remove_widget(self.frequency)
        except IndexError:
            self.remove_widget(self.err_message_box)
        except AttributeError:
            self.remove_widget(self.err_message_box)

    def update_textinput_values(self):
        try:
            self.habit_name.text = habits[fetch_index()].name
            self.description.text = habits[fetch_index()].description
            self.goal.text = str(habits[fetch_index()].goal)
        except IndexError:
            pass

    def cancel(self, instance):
        self.update_textinput_values()
        self.manager.current = 'MainScreen'
