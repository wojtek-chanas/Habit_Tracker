import unittest
from datetime import date
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
            # self.assertTrue(habit.description)
            self.assertTrue(habit.goal)
            self.assertTrue(habit.frequency)

        # test that each habit's history list is not empty
        for habit in habits:
            self.assertTrue(habit.history)

        # test that each habit's creation_date is before today's date
        for habit in habits:
            self.assertLess(habit.creation_date, date.today())


class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit('Read', 'Read for 30 minutes a day', 7, 'Days')

    def test_count_streak(self):
        self.assertEqual(self.habit.count_streak(), '-')  # No history yet
        self.habit.history.append(date(2023, 2, 28))
        self.assertEqual(self.habit.count_streak(), '1 day(s)')  # One day streak
        self.habit.history.append(date(2023, 3, 1))
        self.assertEqual(self.habit.count_streak(), '2 day(s)')  # Two day streak
        self.habit.history.append(date(2023, 3, 2))
        self.habit.history.append(date(2023, 3, 3))
        self.habit.history.append(date(2023, 3, 4))
        self.habit.history.append(date(2023, 3, 5))
        self.habit.history.append(date(2023, 3, 6))
        self.assertEqual(self.habit.count_streak(), '7 day(s)')  # Seven day streak
        self.habit.history.append(date(2023, 3, 8))
        self.assertEqual(self.habit.count_streak(), '1 day(s)')  # Broken streak
        self.habit.history.append(date(2023, 3, 10))
        self.habit.history.append(date(2023, 3, 11))
        self.assertEqual(self.habit.count_streak(), '2 day(s)')  # Two day streak
        self.habit.history = []  # Reset back to an empty table

    def test_mark_done(self):
        self.assertEqual(self.habit.history, [])  # No history yet
        self.habit.mark_done()
        self.assertEqual(self.habit.history, [date.today()])  # History contains today's date
        self.habit.mark_done()
        self.assertEqual(self.habit.history, [date.today()])  # History contains today's date only once
        self.habit.history = []  # Reset back to an empty table

    def test_when_done(self):
        self.assertEqual(self.habit.when_done(), 'Not yet')  # No history yet
        self.habit.mark_done()
        self.assertEqual(self.habit.when_done(), date.today().strftime("%d-%m-%Y"))  # Last date is today's date
        self.habit.mark_done()
        self.assertEqual(self.habit.when_done(), date.today().strftime("%d-%m-%Y"))  # Last date is still today's date
        self.habit.history = []  # Reset back to an empty table

    def test_count_progress(self):
        self.assertEqual(self.habit.count_progress(), '0/7')  # No history yet
        self.habit.history.append(date(2023, 3, 2))
        self.assertEqual(self.habit.count_progress(), '1/7')  # One mark in history
        self.habit.mark_done()
        self.assertEqual(self.habit.count_progress(), '2/7')  # Two marks in history
        self.habit.history = [date.today()] * 7
        self.assertEqual(self.habit.count_progress(), '7/7')  # Goal achieved
        self.habit.history = []  # Reset

    def test_is_completed(self):
        self.habit.is_completed()
        self.assertFalse(self.habit.isCompleted)  # Not completed yet
        self.habit.history = [date(2023, 3, 6), date(2023, 3, 7), date(2023, 3, 8), date(2023, 3, 9), date(2023, 3, 12),
                              date(2023, 3, 14), date(2023, 3, 17)]
        self.habit.is_completed()
        self.assertTrue(self.habit.isCompleted)  # Completed successfully
        self.habit.history.append(date(2023, 3, 23))
        self.habit.is_completed()
        self.assertTrue(self.habit.isCompleted)  # Exceeded goal


if __name__ == '__main__':
    unittest.main()
