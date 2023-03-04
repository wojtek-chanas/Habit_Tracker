from datetime import date, timedelta


class Habit:
    def __init__(self, name, description, goal, frequency):
        self.congratulate = False
        self.index = None
        self.streak = 1
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
        # Check if self.history isn't empty
        if len(self.history) == 0:
            return '-'
        elif self.frequency == 'Days':
            self.streak = 0
            for i in range(0, len(self.history)):
                if sorted_history[i] - sorted_history[i - 1] <= timedelta(days=1):
                    self.streak += 1

                    # update the longest streak if current streak is longer
                    if self.streak > self.longest_streak:
                        self.longest_streak = self.streak

                elif sorted_history[i] - sorted_history[i - 1] > timedelta(days=1):  # break the streak
                    self.streak = 1

                elif len(self.history) == 1:
                    self.streak = 1

            outcome = f'{self.streak} day(s)'
            return outcome

        elif self.frequency == 'Weeks':
            for i in range(0, len(self.history)):
                # datetime.date.isocalendar() allows to compare week numbers, so the amount of days in between each
                # completion of the habit doesn't matter, as long as it's marked completed in two consecutive weeks
                if sorted_history[i].isocalendar().week - sorted_history[i - 1].isocalendar().week == 1:
                    self.streak += 1
                    # update the longest streak if current streak is longer
                    if self.streak > self.longest_streak:
                        self.longest_streak = self.streak

                elif sorted_history[i].isocalendar().week == sorted_history[i - 1].isocalendar().week:
                    # If done more than once in same week
                    self.streak = self.streak

                elif sorted_history[i].isocalendar().week - sorted_history[i - 1].isocalendar().week > 1:
                    # Break the streak
                    self.streak = 1

                elif len(self.history) == 1:
                    self.streak = 1
                else:
                    pass
            outcome = f'{self.streak} week(s)'
            return outcome

        elif self.frequency == 'Months':
            for i in range(0, len(self.history)):
                # compare month numbers and add extra condition for habit done consecutively in december and january
                if sorted_history[i].month - sorted_history[i - 1].month == 1 or \
                        (sorted_history[i].month == 1 and sorted_history[i - 1].month == 12) and sorted_history[i].year\
                        - sorted_history[i-1].year == 1:
                    self.streak += 1
                    # update the longest streak if current streak is longer
                    if self.streak > self.longest_streak:
                        self.longest_streak = self.streak

                # Break the streak
                elif sorted_history[i].month - sorted_history[i - 1].month > 1:
                    self.streak = 1

                # don't change anything if habit was done multiple times in the same month
                elif sorted_history[i].month == sorted_history[i - 1].month:
                    self.streak = self.streak

                # set streak to 1 once the habit is completed for the first time
                elif len(self.history) == 1:
                    self.streak = 1
                else:
                    pass
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
            # The user just achieved the target
            if int(len(self.history))/int(self.goal) == 1:
                self.isCompleted = True
                self.congratulate = True
            # The user exceeded the goal
            elif int(len(self.history))/int(self.goal) >= 1:
                self.isCompleted = True
                self.congratulate = False
            # Nothing to celebrate yet
            else:
                self.isCompleted = False
                self.congratulate = False

        except ValueError or ZeroDivisionError:
            self.goal = '1'
            self.count_progress()
            self.isCompleted = False
            self.congratulate = False
