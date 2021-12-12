import os
from runner import Runner

class ConcreteRunner(Runner):
    """ Runner for Python 3.10 running Queen.py for multiple widths. """

    PYTHON_VERSION = '3.10'

    def __init__(self):
        """ Initialize. """
        self.logFileName = 'results/python_%s_%s.py.log' % (ConcreteRunner.PYTHON_VERSION, self.get_timestamp())

    def get_log(self):
        """ Define concrete log file. """
        return self.logFileName

    def run(self):
        """ Running the queen algorithm for multiple widths. """       
        self.log('SOURCE=Queen.py')
        self.log('VERSION=Python %s' % ConcreteRunner.PYTHON_VERSION)
        self.log('TIMESTAMP=%s' %  self.get_timestamp())

        self.execute('docker pull python:%s' % ConcreteRunner.PYTHON_VERSION)

        for width in range(8, 15+1):
            print('Queen %(width)dx%(width)d' % {'width': width})
            self.execute('docker run -it --rm --name queen-python -v "%s\src:/usr/src" -w /usr/src python:%s python ./Queen.py %d >> %s' % 
                (os.getcwd(), ConcreteRunner.PYTHON_VERSION, width, self.get_log()))

if __name__ == "__main__":
    concrete = ConcreteRunner()
    concrete.run()