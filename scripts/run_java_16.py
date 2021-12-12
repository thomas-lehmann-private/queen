import os
from runner import Runner

class ConcreteRunner(Runner):
    """ Runner for Java running Queen.java for multiple widths. """

    JAVA_VERSION = '16'

    def __init__(self):
        """ Initialize. """
        self.logFileName = 'results/java_%s_%s.java.log' % (ConcreteRunner.JAVA_VERSION, self.get_timestamp())

    def get_log(self):
        """ Define concrete log file. """
        return self.logFileName

    def run(self):
        """
        Running the queen algorithm for multiple widths.
        :see: https://hub.docker.com/_/openjdk/
        """       
        self.log('SOURCE=Queen.java')
        self.log('VERSION=Java %s' % ConcreteRunner.JAVA_VERSION)
        self.log('TIMESTAMP=%s' %  self.get_timestamp())

        self.execute('docker pull openjdk:%s' % ConcreteRunner.JAVA_VERSION)

        for width in range(8, 16+1):
            print('Queen %(width)dx%(width)d' % {'width': width})
            self.execute('docker run -it --rm --name queen-java -v "%s\src:/usr/src" -w /usr/src openjdk:%s java ./Queen.java %d >> %s' % 
                (os.getcwd(), ConcreteRunner.JAVA_VERSION, width, self.get_log()))

if __name__ == "__main__":
    concrete = ConcreteRunner()
    concrete.run()
