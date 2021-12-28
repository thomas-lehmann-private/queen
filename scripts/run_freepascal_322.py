import os
from runner import Runner

class ConcreteRunner(Runner):
    """ Runner for Freepascal running Queen.pas for multiple widths. """

    PASCAL_VERSION = '3.2.2'

    def __init__(self):
        """ Initialize. """
        self.logFileName = 'results/freepascal_%s_%s.pas.log' % (ConcreteRunner.PASCAL_VERSION, self.get_timestamp())

    def get_log(self):
        """ Define concrete log file. """
        return self.logFileName

    def run(self):
        """
        Running the queen algorithm for multiple widths.
        :see: https://github.com/kveroneau/fpc-docker
        """       
        self.log('SOURCE=Queen.pas')
        self.log('VERSION=Freepascal %s' % ConcreteRunner.PASCAL_VERSION)
        self.log('TIMESTAMP=%s' %  self.get_timestamp())

        self.execute('docker pull kveroneau/fpc:%s' % ConcreteRunner.PASCAL_VERSION)

        for width in range(8, 16+1):
            print('Queen %(width)dx%(width)d' % {'width': width})
            self.execute('docker run -it --rm --name queen-freepascal -v "%s\src:/usr/src" -w /usr/src kveroneau/fpc:%s bash -c "fpc -O4 -o/tmp/Queen ./Queen.pas && /tmp/Queen %d">> %s' % 
                (os.getcwd(), ConcreteRunner.PASCAL_VERSION, width, self.get_log()))

if __name__ == "__main__":
    concrete = ConcreteRunner()
    concrete.run()
