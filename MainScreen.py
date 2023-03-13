from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from MetricsScreen import FrameBoxLayout
from functions import habits
from data import save_changes

# Initialize global variable used to access objects from habits list
current_habit_index = 0


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.table_filter_button = None
        self.table_view_box = None
        self.table_view = None
        self.table_view_options = None
        self.selected_habit = None
        self.selected_habit_box = None
        self.table = None

    def on_enter(self, *args):
        # Create add button
        add_button = Button(text='Add Habit', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.4, 'center_y': 0.06})
        add_button.bind(on_release=self.add_window)

        # Create metrics button
        metrics_button = Button(text='Metrics', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.6, 'center_y': 0.06})
        metrics_button.bind(on_release=self.goto_metrics)

        # Create 'mark done' button
        mark_done_button = Button(text='Mark done', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.6, 'center_y': 0.16})
        mark_done_button.bind(on_release=self.mark_done_in_habits)
        self.add_widget(mark_done_button)
    
        # Create edit button
        edit_button = Button(text='Edit', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.4, 'center_y': 0.16})
        edit_button.bind(on_release=self.go_to_menu)
        self.add_widget(edit_button)

        # Create details button
        details_button = Button(text='Habit Details', size_hint=(0.4, 0.05),
                                pos_hint={'center_x': 0.5, 'center_y': 0.235})
        details_button.bind(on_release=self.goto_details)
        self.add_widget(details_button)

        # Filter list by periodicity
        self.table_view_options = Spinner(values=("all", "daily", "weekly", "monthly", "completed"), text='all',
                                          size_hint=(0.4, None), font_size=18,
                                          height=20,
                                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                          )

        self.table_filter_button = Button(text='filter', size_hint=(0.4, None), font_size=18, height=20,
                                          pos_hint={'center_x': 0.7, 'center_y': 0.5}, on_release=self.filter_table)

        self.table_view = MDLabel(text=" show habits: ", font_size=24, height=20, padding_x=1,
                                  size_hint=(0.4, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.table_view_box = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.05), spacing=0,
                                        pos_hint={'center_x': 0.77, 'center_y': 0.28})
        
        # Add widgets to the box
        self.table_view_box.add_widget(self.table_view)
        self.table_view_box.add_widget(self.table_view_options)
        self.table_view_box.add_widget(self.table_filter_button)

        # Add widgets to the screen
        self.add_widget(self.table_view_box)
        self.add_widget(metrics_button)
        self.add_widget(add_button)

        # Display the data table
        self.load_table()
        
        # Display selected habit
        self.show_selected_habit()

    def load_table(self):
        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            size_hint=(0.95, 0.65),
            use_pagination=True,
            check=False,
            column_data=[
                ("Nr", dp(10)),
                ("Habit", dp(30)),
                ("Description", dp(50)),
                ('Last done', dp(20)),
                ("Current streak", dp(20)),
                ("Progress", dp(15))],
        )

        self.filter_table()
        self.table.bind(on_row_press=self.row_press)
        self.add_widget(self.table)

    def goto_metrics(self, *args):
        self.manager.current = 'MetricsScreen'

    def goto_details(self, *args):
        self.manager.current = 'HabitDetailsScreen.py'

    def on_leave(self, *args):
        self.clear_widgets()

    def row_press(self, table, row):
        self.get_row_index(table, row)

    def get_row_index(self, table, row):
        try:
            # get start index from selected row item range
            start_index, end_index = row.table.recycle_data[row.index]['range']
            global current_habit_index
            current_habit_index = int(row.table.recycle_data[start_index]["text"])-1
            # deduct 1 from current_habit_index to adjust for zero-indexing
            print("current_index= ", current_habit_index)
            self.show_selected_habit()
            return current_habit_index
        except IndexError:
            pass

    def mark_done_in_habits(self, *args):
        try:
            habits[current_habit_index].mark_done()
            habits[current_habit_index].streak_st()
            save_changes(habits)
            # Update the table
            self.remove_widget(self.table)
            # self.remove_widget(self.selected_habit_box)
            self.load_table()
            self.show_selected_habit()
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

        except IndexError:
            pass

    def go_to_menu(self, *args):
        self.manager.current = 'EditScreen'

    def add_window(self, *args):
        self.manager.current = 'Add new habit'

    def show_selected_habit(self):
        try:
            self.selected_habit = MDLabel(text=f'Selected habit:  {habits[current_habit_index].name}',
                                          font_size=24, size_hint=(0.9, 0.9), height=50,
                                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        except IndexError:
            self.selected_habit = MDLabel(text=f'Selected habit:  it\'s empty here',
                                          font_size=24, size_hint=(0.9, 0.9), height=50,
                                          pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.selected_habit_box = FrameBoxLayout(orientation='vertical', size_hint=(0.4, 0.05),
                                                 pos_hint={'center_x': 0.255, 'center_y': 0.37})

        self.selected_habit_box.add_widget(self.selected_habit)
        self.add_widget(self.selected_habit_box)

    def filter_table(self, *args):
        for habit in habits:  # Refresh streaks
            habit.count_streak()
        if self.table_view_options.text == "all":

            self.table.row_data = [(habit.index + 1, habit.name, habit.description, habit.when_done(),
                                    habit.streak_st(), habit.count_progress()) for habit in habits]

        elif self.table_view_options.text == "daily":

            self.table.row_data = [(habit.index + 1, habit.name, habit.description, habit.when_done(),
                                    habit.streak_st(), habit.count_progress()) for habit in habits
                                   if habit.frequency == "Days"]

        elif self.table_view_options.text == "weekly":

            self.table.row_data = [(habit.index + 1, habit.name, habit.description, habit.when_done(),
                                    habit.streak_st(), habit.count_progress()) for habit in habits
                                   if habit.frequency == "Weeks"]

        elif self.table_view_options.text == "monthly":

            self.table.row_data = [(habit.index + 1, habit.name, habit.description, habit.when_done(),
                                    habit.streak_st(), habit.count_progress()) for habit in habits
                                   if habit.frequency == "Months"]

        elif self.table_view_options.text == "completed":

            self.table.row_data = [(habit.index + 1, habit.name, habit.description, habit.when_done(),
                                    habit.streak_st(), habit.count_progress()) for habit in habits
                                   if habit.isCompleted]

        return self.table.row_data
