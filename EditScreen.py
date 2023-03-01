from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
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
        self.habit_name = MDTextField(hint_text='Change habit name', text=habits[fetch_index()].name, mode="fill",
                                      helper_text='Name can\'t be empty.', required=True,
                                      helper_text_mode='on_error', font_size=24, size_hint=(0.9, None), height=50,
                                      pos_hint={'center_x': 0.5, 'center_y': 0.9})

        self.description = MDTextField(hint_text='Description', text=habits[fetch_index()].description, mode="fill",
                                       helper_text='Type in a new description.', helper_text_mode='on_focus',
                                       font_size=24, size_hint=(0.9, None), height=50,
                                       pos_hint={'center_x': 0.5, 'center_y': 0.7})

        self.goal = MDTextField(hint_text='Goal', text=habits[fetch_index()].goal, mode="fill",
                                helper_text='The goal must be an integer larger than 0', required=True,
                                helper_text_mode='on_error', font_size=24, size_hint=(0.9, None), height=50,
                                pos_hint={'center_x': 0.5, 'center_y': 0.5}, input_filter=positive_int_input_filter)
        
        self.frequency = Spinner(values=("Days", "Weeks", "Months"), font_size=24, size_hint_y=None, height=50,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.35},
                                 text=habits[fetch_index()].frequency)
        
        self.add_widget(self.habit_name)
        self.add_widget(self.description)
        self.add_widget(self.goal)
        self.add_widget(self.frequency)

    def confirm_dbox(self, *args):
        """ Displays dialog box to confirm habit deletion """
        delete_button = MDFlatButton(text='Delete', on_release=self.delete)
        cancel_button = MDFlatButton(text='Cancel', on_release=self.dbox_cancel)
        self.dialog = MDDialog(title='Delete Habit', text=f'Are you sure? Habit: {habits[fetch_index()].name} '
                                                          f'and its data will be lost.',
                               size_hint=(0.6, 0.2),
                               buttons=[delete_button, cancel_button])
        self.dialog.open()

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
        """ Reassigns Habit object attributes name, description and goal using TextField's values.  """
        if not self.habit_name.text == "" and not self.goal.text == "" and self.frequency.text in ("Days", "Weeks", "Months"):
            habits[fetch_index()].name = self.habit_name.text
            habits[fetch_index()].description = self.description.text
            habits[fetch_index()].goal = self.goal.text
            save_changes(habits)
            print("Changes has been saved.")
            self.manager.current = 'MainScreen'
        else:
            pass

    def on_leave(self, *args):
        """ Clears the text fields """
        self.habit_name.text = self.habit_name.hint_text = self.habit_name.helper_text = ""
        self.habit_name.clear_widgets()
        self.description.text = ""
        self.description.clear_widgets()
        self.goal.text = self.goal.hint_text = self.goal.helper_text = ""
        self.goal.clear_widgets()
        self.frequency.clear_widgets()

    def update_textinput_values(self):
        self.habit_name.text = habits[fetch_index()].name
        self.description.text = habits[fetch_index()].description
        self.goal.text = str(habits[fetch_index()].goal)

    def cancel(self, instance):
        self.update_textinput_values()
        self.manager.current = 'MainScreen'
