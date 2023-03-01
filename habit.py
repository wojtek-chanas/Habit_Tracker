from datetime import date, timedelta


class Habit:
    def __init__(self, name, description, goal, frequency):
        self.congratulate = False
        self.index = None
        self.streak = 0
        self.name = name
        self.description = description
        self.goal = goal
        self.history = []
        self.progress = ""
        self.isCompleted = None
        self.frequency = frequency
        self.longest_streak = 0

    def count_streak(self):
        """ Returns current day-streak. """
        sorted_history = sorted(self.history, reverse=False)
        self.streak = 0
        # Check if self.history isn't empty
        if len(self.history) == 0:
            return '-'
        elif self.frequency == 'Days':
            for i in range(0, len(self.history)):
                if sorted_history[i] - sorted_history[i - 1] <= timedelta(days=1):
                    self.streak += 1

                    # update the longest streak if current streak is longer
                    if self.streak > self.longest_streak:
                        self.longest_streak = self.streak
                else:
                    self.streak = 1
            outcome = f'{self.streak} day(s)'
            return outcome

        elif self.frequency == 'Weeks':
            for i in range(0, len(self.history)):
                if sorted_history[i] - sorted_history[i - 1] <= timedelta(days=7):
                    self.streak += 1
                    # update the longest streak if current streak is longer
                    if self.streak > self.longest_streak:
                        self.longest_streak = self.streak
                else:
                    self.streak = 1
            outcome = f'{self.streak} week(s)'
            return outcome

        elif self.frequency == 'Months':
            for i in range(0, len(self.history)):
                if sorted_history[i] - sorted_history[i - 1] <= timedelta(days=30):
                    self.streak += 1
                    # update the longest streak if current streak is longer
                    if self.streak > self.longest_streak:
                        self.longest_streak = self.streak
                else:
                    self.streak = 1
            outcome = f'{self.streak} month(s)'
            return outcome

    def mark_done(self):
        """ Method marks the habit as done, by appending current date to the self.history table """
        if not date.today() in self.history:
            self.history.append(date.today())
        self.is_completed()

    def when_done(self):
        """ Returns the latest date when the habit has been marked as done, if self.history is empty it returns string
        'not yet' """
        if len(self.history) == 0:
            return 'Not yet'
        else:
            return self.history[-1].strftime("%d-%m-%Y")

    def count_progress(self):
        """ Assigns and returns self.progress attribute.  """
        self.progress = f"{len(self.history)}/{self.goal}"
        return self.progress

    def is_completed(self):
        """ Method checks whether the habit's goal can be recognized as accomplished  """
        try:
            # The user just achieved the target, thus #party_time
            if int(len(self.history))/int(self.goal) == 1:
                self.isCompleted = True
                self.congratulate = True
            # The user exceeded the goal, don't trigger congratulate pop-ups anymore
            elif int(len(self.history))/int(self.goal) >= 1:
                self.isCompleted = True
                self.congratulate = False
            # Nothing to celebrate yet
            else:
                self.isCompleted = False
                self.congratulate = False

        except ValueError or ZeroDivisionError:
            print("ValueError occurred in Habit-class method is_completed(). \n Goal changed to 1.")
            self.goal = '1'
            self.count_progress()
            self.isCompleted = False
            self.congratulate = False





