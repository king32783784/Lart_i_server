import os
import linecache
import time
from parsing_xml import Parsing_XML


def testxmllocate(xmlfile):
    homedir = os.popen('pwd').read().strip('\n')
    local_xmlfile = os.path.join(homedir, xmlfile)
    return local_xmlfile


class ReadPublicinfo(Parsing_XML):
    setupxml = testxmllocate("Testsetup_sample.xml")
    testparameterxml = testxmllocate("Test_parameter.xml")

    def __init__(self):
        self.osname = self.os_name()
        self.setupinfo = self.setup_info()
        self.dotestlist = self.testlists()

    def os_name(self):
        f = open('/etc/os-release', 'r')
        theline = linecache.getline("/etc/os-release", 5)
        osname_line = theline[13:-2]
        osname = osname_line.replace(' ', '_')
        return osname

    def setup_info(self):
        '''
           test_setup_info is Dictionary.
           'xml_list': ['testqurey', 'testtype', 'default',
            'defperf', 'definfo', 'defstab', 'deffun', 'cusperf',
            'cusinfo', 'cusstab', 'cusfun']
            'xml_dict': {'testqurey': ['yes'], 'testtype': ['default'],
            'default':['performance'], 'defperf':['Perf_cpu'],
            'definfo':['Hwinfo'], 'dfstab':['Stb_cpu'], 'deffun':
            ['Fun_kernel'], 'cusperf':['Perf_cpu'],'cusinfo':[],'cusstab'
            :[],'cusfun':[]
        '''
        test_setup = Parsing_XML(self.setupxml, 'setuptype')
        test_setup_info = test_setup.specific_elements()
        return test_setup_info

    def testlists(self):
        tmpdict = self.setupinfo['xml_dict']
        dotestlist = {}
        if tmpdict['testtype'][0] == 'default':
            testtypelist = tmpdict['default'][0].split(' ')
            for testtype in testtypelist:
                if testtype == "performance":
                    dotestlist['performance'] = tmpdict['defperf'][0].split(' ')
                elif testtype == "info":
                    dotestlist['info'] = tmpdict['definfo'][0].split(' ')
                elif testtype == "stability":
                    dotestlist['stability'] = tmpdict['defstab'][0].split(' ')
                elif testtype == "function":
                    dotestlist['function'] = tmpdict['defun'][0].split(' ')
        if tmpdict['testtype'][0] == 'custom':
            testtypelist = tmpdict['custom'][0].split(' ')
            for testtype in testtypelist:
                if testtype == "performance":
                    dotestlist['performance'] = tmpdict['cusperf'][0].split(' ')
                elif testtype == "info":
                    dotestlist['info'] = tmpdict['cusinfo'][0].split(' ')
                elif testtype == "stability":
                    dotestlist['stability'] = tmpdict['cusstb'][0].split(' ')
                elif testtype == "function":
                    dotestlist['function'] = tmpdict['cusfun'][0].split(' ')
        return dotestlist
# TEST
# a=ReadPublicinfo()
# testtypelist = a.setupinfo['xml_dict']['defperf'][0].split(' ')
# print testtypelist
# print a.setupinfo['xml_dict']['defperf']
# testlist = a.testlists()
# print testlist
