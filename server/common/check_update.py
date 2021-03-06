import urllib2
import re
import os
import logging
from subprocess import Popen, PIPE
from downloadfile import downloadfile
from public import ReadPublicinfo

lartlogger = logging.getLogger('Lart_i_server')


class Check_Update(ReadPublicinfo):
    def __init__(self):
        ReadPublicinfo.__init__(self)
        self.setup = self.setup_info()
        self.isoname = self.getisoname()

    def get_htmlcontent(self, xmlurl, remode):
        try:
            html_Context = urllib2.urlopen(xmlurl).read()
        except urllib2.HTTPError:
            lartlogger.error('%s is open failed' % xmlurl)  # need report this error  to tester by mail
        html_Context = unicode(html_Context, 'utf-8')
        return re.findall(r"%s" % remode, html_Context)

    def getisoname(self):
        xmlurl = self.setup['xml_dict']['isourl'][0]
        remode = "href=\"(.+).iso\">"
        targetiso = self.get_htmlcontent(xmlurl, remode)
        if len(targetiso) == 1:
            return targetiso[0] + '.iso'
        elif len(targetiso) < 1:
            return targetiso  # need report this error  to tester by mail
        else:
            getiso = targetiso[0]
            for iso in targetiso:
                if iso > getiso:
                    getiso = iso
            return getiso + '.iso'

    def getisomd5(self, testiso):
        xmlurl = os.path.join(self.setup['xml_dict']['isourl'][0],
                              testiso) + '.md5sum'
        remode = "(.+)"
        lartlogger.info(xmlurl)
        targetmd5 = self.get_htmlcontent(xmlurl, remode)
        return targetmd5[0]

    def downloadiso(self, testiso):
        locatedir = os.path.join(self.setup['xml_dict']['isoserver'][0],
                                 testiso)
        isourl = os.path.join(self.setup['xml_dict']['isourl'][0],
                              testiso) 
        downloadfile(locatedir, isourl)
        filemdsum = Popen('md5sum %s' % locatedir, stdout=PIPE, shell=True)
        filemd5=filemdsum.communicate()[0]
        md5standard = self.getisomd5(testiso)
        if filemd5[0:32] == md5standard[0:32]:
            return "yes"
        else:
            return "no"

    def mountiso(self, testiso):
        cmds = 'mount -t iso9660 -o loop /var/www/html/testiso/%s /var/www/html/testingiso' % testiso
        mountstatus = os.system('%s' % cmds)
        if mountstatus != 0:
            lartlogger.error('mount testiso faild,please chech it')  # need to mail
