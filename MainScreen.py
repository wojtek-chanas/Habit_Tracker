from kivy.metrics import dp
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from functions import habits
from data import save_changes

# Initialize global variable used to access objects from habits list
current_habit_index = 0


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = None

    def on_enter(self, *args):
        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint=(0.95, 0.75),
            use_pagination=True,
            check=False,
            column_data=[
                ("Nr", dp(10)),
                ("Habit", dp(30)),
                ("Description", dp(50)),
                ('Last done', dp(20)),
                ("Current streak", dp(20)),
                ("Progress", dp(15))],
            row_data=[(habit.index + 1, habit.name, habit.description, habit.when_done(), habit.count_streak(),
                       habit.count_progress()) for habit in habits])  # habit.index + 1 so numbers won't start from 0

        self.table.bind(on_row_press=self.row_press)

        add_button = Button(text='Add Habit', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.4, 'center_y': 0.06})
        add_button.bind(on_release=self.add_window)
        self.add_widget(add_button)
        self.add_widget(self.table)

        metrics_button = Button(text='Metrics', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.6, 'center_y': 0.06})
        metrics_button.bind(on_release=self.goto_metrics)
        self.add_widget(metrics_button)

    def goto_metrics(self, *args):
        self.manager.current = 'MetricsScreen'

    def on_leave(self, *args):
        self.clear_widgets()

    def row_press(self, table, row):
        self.get_row_index(table, row)
        self.my_temp_fun()

    def get_row_index(self, table, row):
        # get start index from selected row item range
        start_index, end_index = row.table.recycle_data[row.index]['range']
        global current_habit_index
        current_habit_index = int(row.table.recycle_data[start_index]["text"])-1  # deduct 1 to adjust for zero-indexing
        print("current_index= ", current_habit_index)

    def my_temp_fun(self):
        def mark_done_in_habits(*args):
            habits[current_habit_index].mark_done()
            save_changes(habits)
            # Update the table
            self.on_leave()
            self.on_enter()
            # Check if the goal is reached, if so display a congrats popup
            if habits[current_habit_index].isCompleted and habits[current_habit_index].congratulate:
                def close_popup(*args):
                    self.dialog.dismiss()
                awesome_button = MDFlatButton(text='Awesome!', on_release=close_popup)
                # Check habit's frequency and get matching text to use in congrats pop-up
                if habits[current_habit_index].frequency == 'Days':
                    period = 'day(s)'
                elif habits[current_habit_index].frequency == 'Months':
                    period = 'month(s)'
                else:
                    period = 'week(s)'
                # Display a pop-up
                self.dialog = MDDialog(title='Congratulations!', text=f'You reached your goal of keeping your habit '
                                                                      f'"{habits[current_habit_index].name}" for '
                                                                      f'{habits[current_habit_index].goal} {period}.',
                                       size_hint=(0.6, 0.2),
                                       buttons=[awesome_button])
                self.dialog.open()

        mark_done_button = Button(text='Mark done', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.6, 'center_y': 0.16})
        mark_done_button.bind(on_release=mark_done_in_habits)
        self.add_widget(mark_done_button)

        def go_to_menu(*args):
            self.manager.current = 'EditScreen'

        edit_button = Button(text='Edit', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.4, 'center_y': 0.16})
        edit_button.bind(on_release=go_to_menu)
        self.add_widget(edit_button)

    def add_window(self, *args):
        self.manager.current = 'Add new habit'
