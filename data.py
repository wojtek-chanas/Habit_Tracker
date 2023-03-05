import pickle


def save_changes(habits):
    """ Saves habits list in a habits.pkl file """
    with open("habits.pkl", "wb") as f:
        pickle.dump(habits, f, protocol=4)


def load_habits():
    """ Returns list of Habit class objects from a habits.pkl file, or returns an empty list if file doesn't exist  """
    class UnpicklerWithClasses(pickle.Unpickler):
        def find_class(self, module, name):
            if module == "__main__":
                module = "main"
            return super().find_class(module, name)

    try:
        with open('habits.pkl', 'rb') as f:
            habits = UnpicklerWithClasses(f).load()
            return habits
    # If file doesn't exist return an empty list
    except FileNotFoundError:
        return []
