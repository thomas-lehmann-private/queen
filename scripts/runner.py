import os
import time
import datetime
  
class Runner:
    """ Base class for runner """

    def get_log(self):
        """ Forcing implementation of path and filename for current log. """
        raise 'Missing get_log(self) implementation!'

    def get_timestamp(self):
        """ Get current date as unix timestamp. """
        now = datetime.datetime.now()
        return int(datetime.datetime.timestamp(now) * 1000)

    def log(self, message):
        """ Append message to log file. """
        assert isinstance(message, str)

        with open(self.get_log(), 'a') as handle:
            handle.write(message)
            handle.write('\n')

    def execute(self, command):
        """ Execute shell command. """
        assert isinstance(command, str)
        os.system(command)