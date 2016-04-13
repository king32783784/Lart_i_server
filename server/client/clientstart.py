#!/usr/bin/env python
# coding=utf8
'''
   Name:Linux automated regression testing
   Function:Check the ISO changes
   Author:peng.li@i-soft.com.cn
   Time:20160413
'''


if __name__ == "__main__":
    testxml = ReadPublicinfo()
    setupinfo = testxml.setupinfo
    daemon = Main(setupinfo)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "useage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
