'''
    sysbench: System evaluation benchmark
    test: Perf_cpu Perf_mem Perf_mysql
'''
import os
from runtest import RunTest

class DoTest(RunTest):
    def __init__(self, setupxml, testxml, homepath):
        self.setupxml = os.path.abspath(setupxml)
        self.testxml = os.path.abspath(testxml)
        self.homepath = homepath
    
    def _setup(self):
        '''
         Setup before starting test
        '''
        print self.setupxml
        RunTest._depend('gcc', 'make', 'automake', 'libtool')
        srcdir = RunTest._pretesttool(self.setupxml, self.testxml, 'Perf_cpu', self.homepath)
        
        os.chdir(srcdir)
        self._configure('--without-mysql')
        self._make('LIBTOOL=/usr/bin/libtool')

    def _runtest(self):
        basearg = self.baseparameter('Perf_cpu', self.testxml)
        print basearg
        runtimes = basearg['runtimes']
        cpu_max_prime=basearg['cpu_max_prime'].split(',')
        for max_prime in cpu_max_prime:
            cmd = "--test=%s --cpu-max-prime=%s run" % (basearg['test_type'], max_prime)
            RunTest._dotest('sysbench', cmd, runtimes)
# testcase
#a = Perf_cpu('Testsetup_sample.xml', 'Test_parameter.xml')
#a._setup()
#a._runtest()
