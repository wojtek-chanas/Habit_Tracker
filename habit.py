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
        self.creation_date = None
        self.streak_str = None

    def count_streak(self) -> str:
        """ Computes streak value (int), assigns it to streak attribute and returns current streak (str). """
        sorted_history = sorted(self.history, reverse=False)
        today = date.today()
        if self.frequency == 'Days':
            # Check if self.history isn't empty
            if len(self.history) == 0:
                self.streak = 0
            elif today - sorted_history[-1] > timedelta(days=1):
                self.streak = 0
            else:
                self.streak = 0
                for i in range(0, len(self.history)):
                    if sorted_history[i] - sorted_history[i - 1] <= timedelta(days=1):
                        self.streak += 1
                        # update the longest streak if current streak is longer
                        if self.streak >= self.longest_streak:
                            self.longest_streak = self.streak

                    elif sorted_history[i] - sorted_history[i - 1] > timedelta(days=1):  # break the streak
                        self.streak = 1

            outcome = f'{self.streak} day(s)'
            return outcome

        elif self.frequency == 'Weeks':
            if len(self.history) == 0:
                self.streak = 0
            elif today.isocalendar().week - sorted_history[-1].isocalendar().week > 1:
                self.streak = 0
            else:
                self.streak = 1
                for i in range(0, len(self.history)):
                    # datetime.date.isocalendar() allows to compare week numbers, so the amount of days in between each
                    # completion of the habit doesn't matter, as long as it's marked completed in two consecutive weeks
                    if sorted_history[i].isocalendar().week - sorted_history[i - 1].isocalendar().week == 1:
                        self.streak += 1
                        # update the longest streak if current streak is longer
                        if self.streak >= self.longest_streak:
                            self.longest_streak = self.streak

                    elif sorted_history[i].isocalendar().week - sorted_history[i - 1].isocalendar().week > 1:
                        # Break the streak
                        self.streak = 1

            outcome = f'{self.streak} week(s)'
            return outcome

        elif self.frequency == 'Months':
            if len(self.history) == 0:
                self.streak = 0
            elif today.month - sorted_history[-1].month > 1 and not (today.month == 1 and sorted_history[-1].month == 12
                                                                     and today.isocalendar().year
                                                                     - sorted_history[-1].year == 1):
                self.streak = 0
            else:
                self.streak = 1
                for i in range(0, len(self.history)):
                    # compare month numbers and add extra condition for habit done consecutively in december and january
                    if sorted_history[i].month - sorted_history[i - 1].month == 1 \
                            or (sorted_history[i].month == 1 and sorted_history[i - 1].month == 12) \
                            and sorted_history[i].year - sorted_history[i - 1].year == 1:
                        self.streak += 1
                        # update the longest streak if current streak is longer
                        if self.streak >= self.longest_streak:
                            self.longest_streak = self.streak

                    # Break the streak
                    elif sorted_history[i].month - sorted_history[i - 1].month > 1:
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
            dates = sorted(self.history)
            return dates[-1].strftime("%d-%m-%Y")

    def count_progress(self) -> str:
        """ Assigns and returns self.progress attribute.  """
        counter = 1
        try:
            sorted_history = sorted(self.history, reverse=False)
            if self.frequency == 'Days':
                counter = 0
                for i in range(0, len(self.history)):
                    counter += 1
            elif self.frequency == 'Weeks':
                for i in range(0, len(self.history)):
                    # datetime.date.isocalendar() allows to compare week numbers, so the amount of days in between each
                    # completion of the habit doesn't matter, as long as it's marked completed in two consecutive weeks
                    if sorted_history[i].isocalendar().week - sorted_history[i - 1].isocalendar().week == 1:
                        counter += 1
            elif self.frequency == 'Months':
                for i in range(0, len(self.history)):
                    # compare month numbers and add extra condition for habit done consecutively in december and january
                    if sorted_history[i].month - sorted_history[i - 1].month == 1 \
                            or (sorted_history[i].month == 1 and sorted_history[i - 1].month == 12) \
                            and sorted_history[i].year - sorted_history[i - 1].year == 1:
                        counter += 1
        except IndexError:
            if len(self.history) == 0:
                counter = 0
            elif len(self.history) == 1:
                counter = 1
        finally:
            self.progress = f"{counter}/{self.goal}"
            return self.progress

    def is_completed(self):
        """ Method checks whether the habit's goal can be recognized as accomplished  """
        try:
            # The user just achieved the target
            if int(len(self.history)) / int(self.goal) == 1:
                self.isCompleted = True
                self.congratulate = True
            # The user exceeded the goal
            elif int(len(self.history)) / int(self.goal) >= 1:
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

    def streak_st(self):
        self.count_streak()
        streak_st = str(self.streak) + " " + self.frequency[:-1].lower() + "(s)"
        self.streak_str = streak_st
        return self.streak_str
