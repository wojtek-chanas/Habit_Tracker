import unittest
from datetime import date, timedelta
from freezegun import freeze_time
import data
from habit import Habit
from demo import demo_add_habit
from functions import habits


class TestDemoAddHabit(unittest.TestCase):

    def test_add_habit(self):
        # test that 5 habits are added to the global habits list
        demo_add_habit()
        self.assertEqual(len(habits), 5)

        # test that each habit has a name, description, goal, and frequency
        for habit in habits:
            self.assertTrue(habit.name)
            self.assertTrue(habit.goal)
            self.assertTrue(habit.frequency)

        # test that each habit's history list is not empty
        for habit in habits:
            self.assertTrue(habit.history)

        # test that each habit's creation_date is before today's date
        for habit in habits:
            self.assertLess(habit.creation_date, date.today())

    def tearDown(self) -> None:
        global habits
        habits = []
        data.save_changes(habits)


class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit('Read', 'Read for 30 minutes a day', 7, 'Days')

    @freeze_time('2023-03-08')
    def test_count_streak_daily(self):
        self.assertEqual(self.habit.count_streak(), '0 day(s)')  # No history yet
        self.habit.history.append(date(2023, 3, 8))
        self.assertEqual(self.habit.count_streak(), '1 day(s)')  # One day streak
        self.habit.history.append(date(2023, 3, 7))
        self.assertEqual(self.habit.count_streak(), '2 day(s)')  # Two day streak
        self.habit.history.append(date(2023, 3, 6))
        self.habit.history.append(date(2023, 3, 5))
        self.habit.history.append(date(2023, 3, 4))
        self.habit.history.append(date(2023, 3, 3))
        self.habit.history.append(date(2023, 3, 2))
        self.assertEqual(self.habit.count_streak(), '7 day(s)')  # Seven day streak
        self.habit.history = []  # Reset back to an empty table
        self.habit.history.append(date(2023, 3, 6))
        self.habit.history.append(date(2023, 3, 5))
        self.habit.history.append(date(2023, 3, 4))
        self.habit.history.append(date(2023, 3, 3))
        self.habit.history.append(date(2023, 3, 2))
        self.assertEqual(self.habit.count_streak(), '0 day(s)')  # Broken streak
        self.habit.history.append(date(2023, 3, 8))
        self.assertEqual(self.habit.count_streak(), '1 day(s)')  # One-day streak
        self.habit.history = []  # Reset back to an empty table

    @freeze_time('2023-03-08')
    def test_mark_done(self):
        self.assertEqual(self.habit.history, [])  # No history yet
        self.habit.mark_done()
        self.assertEqual(self.habit.history, [date.today()])  # History contains today's date
        self.habit.mark_done()
        self.assertEqual(self.habit.history, [date.today()])  # History contains today's date only once
        self.habit.history = []  # Reset back to an empty table

    @freeze_time('2023-03-08')
    def test_when_done(self):
        self.assertEqual(self.habit.when_done(), 'Not yet')  # No history yet
        self.habit.mark_done()
        self.assertEqual(self.habit.when_done(), date.today().strftime("%d-%m-%Y"))  # Last date is today's date
        self.habit.mark_done()
        self.assertEqual(self.habit.when_done(), date.today().strftime("%d-%m-%Y"))  # Last date is still today's date
        self.habit.history = []  # Reset back to an empty table

    @freeze_time('2023-03-08')
    def test_count_progress(self):
        self.assertEqual(self.habit.count_progress(), '0/7')  # No history yet
        self.habit.history.append(date(2023, 3, 2))
        self.assertEqual(self.habit.count_progress(), '1/7')  # One mark in history
        self.habit.mark_done()
        self.assertEqual(self.habit.count_progress(), '2/7')  # Two marks in history
        self.habit.history = [date.today()] * 7
        self.assertEqual(self.habit.count_progress(), '7/7')  # Goal achieved
        self.habit.history = []  # Reset

    @freeze_time('2023-03-08')
    def test_is_completed(self):
        self.habit.is_completed()
        self.assertFalse(self.habit.isCompleted)  # Not completed yet
        self.habit.history = [date(2023, 3, 6), date(2023, 3, 7), date(2023, 3, 8), date(2023, 3, 9), date(2023, 3, 12),
                              date(2023, 3, 14), date(2023, 3, 17)]
        self.habit.is_completed()
        self.assertTrue(self.habit.isCompleted)  # Completed successfully
        self.habit.history.append(date(2023, 3, 23))
        self.habit.is_completed()
        self.assertTrue(self.habit.isCompleted)
        self.assertFalse(self.habit.congratulate)  # Exceeded goal


class TestWeeklyHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit('Read', 'Read for 30 minutes a day', 7, 'Weeks')

    @freeze_time('2023-03-08')
    def test_count_streak_weekly(self):
        self.assertEqual(self.habit.count_streak(), '0 week(s)')  # No history yet
        self.habit.history.append(date(2023, 2, 28))
        self.assertEqual(self.habit.count_streak(), '1 week(s)')  # One-week streak
        self.habit.history.append(date(2023, 3, 1))
        self.assertEqual(self.habit.count_streak(), '1 week(s)')  # 1 w. since 28-02 and 01-03 are Tuesday and Wednesday
        self.habit.history.append(date(2023, 3, 2))
        self.habit.history.append(date(2023, 3, 3))
        self.habit.history.append(date(2023, 3, 4))
        self.habit.history.append(date(2023, 3, 5))
        self.habit.history.append(date(2023, 3, 6))  # Monday the week after 1st completion date
        self.assertEqual(self.habit.count_streak(), '2 week(s)')  # Two-weeks streak
        self.habit.history.append(date(2023, 3, 17))
        self.assertEqual(self.habit.count_streak(), '3 week(s)')  # Three-weeks streak
        self.habit.history.append(date(2023, 3, 27))  # Broken streak
        self.habit.history.append(date(2023, 4, 4))
        self.assertEqual(self.habit.count_streak(), '2 week(s)')  # Two day streak
        self.habit.history = []  # Reset back to an empty table


class TestMonthlyHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit('Read', 'Read for 30 minutes a day', 7, 'Months')

    @freeze_time('2023-03-08')
    def test_count_streak_monthly(self):
        self.assertEqual(self.habit.count_streak(), '0 month(s)')  # No history yet
        self.habit.history.append(date(2023, 2, 28))
        self.assertEqual(self.habit.count_streak(), '1 month(s)')  # One month streak
        self.habit.history.append(date(2023, 3, 1))
        self.assertEqual(self.habit.count_streak(), '2 month(s)')  # Two month streak
        self.habit.history.append(date(2023, 4, 2))
        self.habit.history.append(date(2023, 5, 14))
        self.habit.history.append(date(2023, 6, 30))
        self.habit.history.append(date(2023, 7, 4))
        self.habit.history.append(date(2023, 8, 20))
        self.assertEqual(self.habit.count_streak(), '7 month(s)')  # Seven month streak
        self.habit.history.append(date(2023, 10, 8))
        self.assertEqual(self.habit.count_streak(), '1 month(s)')  # Broken streak
        self.habit.history = []  # Reset back to an empty table


if __name__ == '__main__':
    unittest.main()
