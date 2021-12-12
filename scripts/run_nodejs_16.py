import os
from runner import Runner

class ConcreteRunner(Runner):
    """ Runner for Nodejs running Queen_node.py for multiple widths. """

    NODE_VERSION = '16'

    def __init__(self):
        """ Initialize. """
        self.logFileName = 'results/javascript_%s_%s.node.js.log' % (ConcreteRunner.NODE_VERSION, self.get_timestamp())

    def get_log(self):
        """ Define concrete log file. """
        return self.logFileName

    def run(self):
        """
        Running the queen algorithm for multiple widths.
        :see: https://hub.docker.com/_/node/
        """       
        self.log('SOURCE=Queen_node.js')
        self.log('VERSION=Nodejs %s' % ConcreteRunner.NODE_VERSION)
        self.log('TIMESTAMP=%s' %  self.get_timestamp())

        self.execute('docker pull node:%s' % ConcreteRunner.NODE_VERSION)

        for width in range(8, 16+1):
            print('Queen %(width)dx%(width)d' % {'width': width})
            self.execute('docker run -it --rm --name queen-nodejs -v "%s\src:/usr/src" -w /usr/src node:%s node ./Queen_node.js %d >> %s' % 
                (os.getcwd(), ConcreteRunner.NODE_VERSION, width, self.get_log()))

if __name__ == "__main__":
    concrete = ConcreteRunner()
    concrete.run()
