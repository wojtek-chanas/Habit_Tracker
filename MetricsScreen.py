from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from functions import habits
from EditScreen import fetch_index
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle


class FrameBoxLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15, ])
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MetricsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = None
        self.longest_weekly = None
        self.longest_daily = None
        self.most_freq_done = None
        self.avg_progress_bar = None
        self.longest_all = None
        self.longest_monthly = None
        back_button = Button(text='Back to menu', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        back_button.bind(on_release=self.back)
        self.add_widget(back_button)

    def back(self, *args):
        self.manager.current = 'MainScreen'
    #     self.update_textinput_values()

    def on_enter(self, *args):
        print('current index= ', fetch_index())

        # The longest streak of all habits
        try:
            longest_streak_all = max([(habit.longest_streak, habit.name, habit.frequency) for habit in habits],
                                     key=lambda x: x[0])
            lgst_strk_all = f" {longest_streak_all[1]}, with a streak of {longest_streak_all[0]} " \
                            f"{longest_streak_all[2].lower()}."
        except ValueError:
            lgst_strk_all = "No habit match the search criteria."
        self.longest_all = MDLabel(text=f'The habit with the longest streak of all habits is \n{lgst_strk_all}',
                                   font_size=24, size_hint=(0.9, 0.9), height=50,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # The most frequently done habit
        try:
            most_freq_done = max([(len(habit.history), habit.name) for habit in habits], key=lambda x: x[0])
            most_freq_done_str = f"{most_freq_done[1]} which has been done {most_freq_done[0]} time(s)"
        except ValueError:
            most_freq_done_str = "No habit match the search criteria."
        self.most_freq_done = MDLabel(text=f'The most frequently done habit is \n{most_freq_done_str}',
                                      font_size=24, size_hint=(0.9, 0.9), height=50,
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # The longest streak of daily habits
        try:
            longest_streak_daily = max([(habit.longest_streak, habit.name) for habit in habits if habit.frequency ==
                                        "Days"], key=lambda x: x[0])
            lgst_strk_daily = f"{longest_streak_daily[1]}, with a streak of {longest_streak_daily[0]} day(s)."
        except ValueError:
            lgst_strk_daily = "No habit match the search criteria."

        self.longest_daily = MDLabel(text=f'The longest streak among daily habits is \n{lgst_strk_daily}',
                                     font_size=24, size_hint=(0.9, 0.9), height=50,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # The longest streak of weekly habits
        try:
            longest_streak_week = max([(habit.longest_streak, habit.name) for habit in habits if habit.frequency ==
                                       "Weeks"], key=lambda x: x[0])
            lgst_strk_weekly = f'{longest_streak_week[1]}, with a streak of {longest_streak_week[0]} week(s).'
        except ValueError:
            lgst_strk_weekly = "No habit match the search criteria."
        self.longest_weekly = MDLabel(text=f'The longest streak among weekly habits is \n{lgst_strk_weekly}',
                                      font_size=24, size_hint=(0.9, 0.9), height=50,
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # The longest streak of monthly habits
        try:
            longest_streak_month = str(max([habit.longest_streak for habit in habits if habit.frequency == "Months"])) \
                                   + "month(s)"
        except ValueError:
            longest_streak_month = "No habit match the search criteria."
        self.longest_monthly = MDLabel(text=f"The longest streak among monthly habits: \n{longest_streak_month}",
                                       font_size=24, size_hint=(0.9, 0.9), height=50,
                                       pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Average progress bar
        avg_progress = self.calculate_avg_progress()
        print(avg_progress)
        self.label = MDLabel(text=f'On average you\'ve reached {round(100*avg_progress, 2)}% of your goal! Keep it up!',
                             pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.9, 0.4))
        self.avg_progress_bar = MDProgressBar(value=int(100*avg_progress), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                              size_hint=(0.9, 0.2))

        # Create FrameBoxLayouts
        longest_daily_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                   'center_y': 0.9})
        longest_weekly_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                    'center_y': 0.79})
        longest_monthly_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                     'center_y': 0.68})
        longest_all_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                 'center_y': 0.57})
        most_freq_done_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                    'center_y': 0.46})
        average_progress_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                      'center_y': 0.35})

        # Add widgets to FrameBoxLayouts
        longest_daily_box.add_widget(self.longest_daily)
        longest_weekly_box.add_widget(self.longest_weekly)
        longest_monthly_box.add_widget(self.longest_monthly)
        longest_all_box.add_widget(self.longest_all)
        most_freq_done_box.add_widget(self.most_freq_done)
        average_progress_box.add_widget(self.label)
        average_progress_box.add_widget(self.avg_progress_bar)

        # Add FrameBoxLayouts to the Screen
        self.add_widget(most_freq_done_box)
        self.add_widget(longest_daily_box)
        self.add_widget(longest_weekly_box)
        self.add_widget(longest_monthly_box)
        self.add_widget(longest_all_box)
        self.add_widget(average_progress_box)

    def calculate_avg_progress(self):
        from functions import habits
        try:
            progress_lst = [len(habit.history)/int(habit.goal) for habit in habits]
            avg_progress = sum(progress_lst)/len(progress_lst)
            print("list: ", progress_lst)
            print("avg_p:", avg_progress)
        except ZeroDivisionError:
            avg_progress = 0
        return avg_progress

    # def on_leave(self, *args):
    #     """ Clears the text fields """
    #     self.clear_widgets()
