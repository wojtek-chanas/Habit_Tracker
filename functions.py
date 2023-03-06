from datetime import date
from habit import Habit
import data

habits = data.load_habits()


def add_habit(name, description, goal, frequency):
    global habits
    flag = True
    for habit in habits:
        if habit.name == name:
            flag = False
    if flag:
        new_habit = Habit(name, description, goal, frequency)
        new_habit.creation_date = date.today()
        habits.append(new_habit)
        new_habit.index = habits.index(new_habit)
        data.save_changes(habits)
    else:
        print("Habit name already exists!")


def delete_habit(index):
    del habits[index]
    data.save_changes(habits)


# Define a function to validate the input for goal value
def positive_int_input_filter(text, from_undo=False):
    """ Checks if goal input is a positive integer larger than 0. If not - returns an empty string to indicate
     the input should be rejected by the MDTextField """

    # MDTextField calls this function on every character, for that reason zero is
    # either always accepted or always rejected - even as a part of valid value, such as 102. Accept zero here
    # and validate the input later in save method
    try:
        value = int(text)
        if value >= 0:
            return str(value)
        else:
            return ""
    except ValueError:
        return ""
