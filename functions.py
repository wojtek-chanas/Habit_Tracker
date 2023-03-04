from datetime import date
from habit import Habit
import data

habits = data.load_habits()


def add_habit(name, description, goal, frequency):
    global habits
    new_habit = Habit(name, description, goal, frequency)
    new_habit.creation_date = date.today()
    habits.append(new_habit)
    new_habit.index = habits.index(new_habit)
    data.save_changes(habits)


def delete_habit(index):
    del habits[index]
    data.save_changes(habits)


# Define a function to validate the input for goal value
def positive_int_input_filter(text, from_undo=False):
    """ Checks if goal input is a positive integer larger than 0. If not - returns an empty string to indicate
     the input should be rejected by the MDTextField """
    try:
        value = int(text)
        if value > 0:
            return str(value)
        else:
            return ""
    except ValueError:
        return ""
