
""" This script creates 5 sample habits with predefined history and streaks """

from habit import Habit
from datetime import date, timedelta
from random import randint
import calendar
import data

habits = data.load_habits()


def get_number_of_days(year, month):
    """ Returns number of days in selected month """
    _, num_days = calendar.monthrange(year, month)
    return num_days


def random_date():
    """ Returns random date in range from 01/01/2023 until yesterday """
    year = randint(2023, date.today().year)
    if year < date.today().year:
        month = randint(1, 12)
        day = randint(1, get_number_of_days(year, month))
    else:
        month = randint(1, date.today().month)
        if month < date.today().month:
            day = randint(1, get_number_of_days(year, month))
        else:
            day = randint(1, date.today().day - 1)
    return date(year, month, day)


def demo_add_habit():
    """ Adds 5 predefined sample habits with description, periodicity and randomly generated data """
    global habits
    i = 0
    while i < 5:
        habits_dict = {0: ("Workout", "Workout at the gym"),
                       1: ("Reading", "Read a book chapter"),
                       2: ("Practice Python", "Solve a challenge"),
                       3: ("Wash dishes", "no words needed for this"),
                       4: ("Meditate", "meditation or breathing exercises")}
        name = habits_dict[i][0]
        description = habits_dict[i][1]
        goal = str(randint(1, 100))
        frequency_set = ["Days", "Weeks", "Months", "Weeks", "Days"]
        frequency = frequency_set[i]
        new_habit = Habit(name, description, goal, frequency)

        habits.append(new_habit)
        new_habit.index = habits.index(new_habit)
        n = randint(1, int(goal))
        random_history = sorted([random_date() for _ in range(n)])
        for _ in random_history:
            new_habit.history.append(_)
            new_habit.count_streak()
            new_habit.is_completed()
        new_habit.creation_date = random_history[0] - timedelta(days=4)
        data.save_changes(habits)
        i += 1
    print("Habits have been added successfully")


demo_add_habit()
