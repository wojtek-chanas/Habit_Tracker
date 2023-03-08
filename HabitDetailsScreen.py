from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from EditScreen import fetch_index
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle
from functions import habits, compute_progress


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


class HabitDetailsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.habit_progress_label = None
        self.error_message = None
        self.longest_streak_label = None
        self.current_streak_label = None
        self.last_done_label = None
        self.first_done_label = None
        self.habit_creation_label = None
        self.habit_name_label = None
        self.habit_progress_bar = None

    def back(self, *args):
        self.manager.current = 'MainScreen'
    #     self.update_textinput_values()

    def on_enter(self, *args):
        try:
            habit = habits[fetch_index()]
            # Name
            self.habit_name_label = MDLabel(text=f"Habit name: {habit.name}", font_size=24, size_hint=(0.9, 0.9),
                                            height=50, pos_hint={'center_x': 0.5, 'center_y': 0.5})

            # Creation date
            self.habit_creation_label = MDLabel(text=f"Created on: {habit.creation_date}", font_size=24,
                                                size_hint=(0.9, 0.9), height=50,
                                                pos_hint={'center_x': 0.5, 'center_y': 0.5})

            # First done on:
            self.first_done_label = MDLabel(text=f"First done on: {habit.history[0]}", font_size=24,
                                            size_hint=(0.9, 0.9), height=50,
                                            pos_hint={'center_x': 0.5, 'center_y': 0.5})

            # Last done on:
            self.last_done_label = MDLabel(text=f"Last done on: {habit.history[-1]}", font_size=24,
                                           size_hint=(0.9, 0.9), height=50,
                                           pos_hint={'center_x': 0.5, 'center_y': 0.5})

            # Current streak
            self.current_streak_label = MDLabel(text=f"Current streak: {habit.streak_str}", font_size=24,
                                                size_hint=(0.9, 0.9), height=50,
                                                pos_hint={'center_x': 0.5, 'center_y': 0.5})

            # Longest streak
            self.longest_streak_label = MDLabel(text=f"Longest streak: {habit.longest_streak}"
                                                     f" {habit.frequency[0:-1].lower()}(s)",
                                                font_size=24, size_hint=(0.9, 0.9), height=50,
                                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            # Progress
            habit_progress = compute_progress()
            self.habit_progress_label = MDLabel(text=f"Goal completion progress: {round(int(100*habit_progress), 2)}%",
                                                font_size=24, size_hint=(0.9, 0.9), height=50,
                                                pos_hint={'center_x': 0.5, 'center_y': 0.5})

            # Create FrameBoxLayouts
            habit_name_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                    'center_y': 0.9})
            habit_creation_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                        'center_y': 0.79})
            first_done_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                    'center_y': 0.68})
            last_done_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                   'center_y': 0.57})
            current_streak_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                        'center_y': 0.46})
            longest_streak_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                        'center_y': 0.24})
            habit_progress_box = FrameBoxLayout(orientation='vertical', size_hint=(0.9, 0.1), pos_hint={'center_x': 0.5,
                                                                                                        'center_y': 0.35})

            # Add widgets to FrameBoxLayouts
            habit_name_box.add_widget(self.habit_name_label)
            habit_creation_box.add_widget(self.habit_creation_label)
            first_done_box.add_widget(self.first_done_label)
            last_done_box.add_widget(self.last_done_label)
            current_streak_box.add_widget(self.current_streak_label)
            longest_streak_box.add_widget(self.longest_streak_label)
            habit_progress_box.add_widget(self.habit_progress_label)

            # Add FrameBoxLayouts to the Screen
            self.add_widget(habit_name_box)
            self.add_widget(habit_creation_box)
            self.add_widget(first_done_box)
            self.add_widget(last_done_box)
            self.add_widget(current_streak_box)
            self.add_widget(longest_streak_box)
            self.add_widget(habit_progress_box)

        except IndexError:
            self.error_message = MDLabel(text=f"Nothing to see here... \nCome back later!", font_size=24,
                                         size_hint=(0.9, 0.9), height=50, halign='center',
                                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
            self.add_widget(self.error_message)

        # Back button
        back_button = Button(text='Back to menu', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        back_button.bind(on_release=self.back)
        self.add_widget(back_button)

    def on_leave(self, *args):
        self.clear_widgets()
