import datetime

class Logger:

    def __init__(self, log_level, component_name):
        self.log_level = log_level
        self.component_name = component_name

    def log(self, log_level, log_message):

        if log_level == self.log_level:
            datum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('\r ' + datum + " :: " + self.component_name + ": " + log_message)
        return