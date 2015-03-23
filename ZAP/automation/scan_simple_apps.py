## Add your environment depending configuration here.
## Otherwise start this script via python scan_simple_apps.py

import time
import os
from pprint import pprint
from zapv2 import ZAPv2

# This is a simple ZAP Wrapper in Python for scanning multible WebApplications in a row
# author: markusmiedaner@gmail.com
# date 2015/03

## !! Attention: ZAP needs to be started in daemon-mode separately !!

# define a list of target urls
targetlist = ['','','']

# define directory where to store session files
sessionPath = 'C:\\Users\\xv01171\\Desktop\\Dummy'

# define directory where to store reports
reportDir = sessionPath + '\\Reports'

# define filenames for session and reports (using one for both)
sessionNames = ['hausrat', 'haftplicht', 'blickUndCheck', 'klinik', 'rechtsschutz']

# counter variable
i = 0

zap = ZAPv2()

# Creating main dir if not existing
if not os.path.exists(sessionPath):
    os.makedirs(sessionPath)

# Creating directory for reports
if not os.path.exists(reportDir):
    os.makedirs(reportDir)


# Loop over all targets, spider them, scan them and generate reports
for target in targetlist:

    print 'Creating session %s' % sessionNames[i]
    zap.core.new_session(sessionPath + '\\' + sessionNames[i])

    print 'Accessing target %s' % target
    zap.urlopen(target)
    time.sleep(2)

    print 'staring spider'
    zap.spider.scan(target)
    time.sleep(2)

    while (int(zap.spider.status) < 100):
        print 'Spider progress %:' + zap.spider.status
        time.sleep(2)

    print 'Spider completed'
    time.sleep(5)

    print 'Scanning target: %s' % target
    zap.ascan.scan(target)

    while (int(zap.ascan.status) < 100):
        print 'Scan progress %:' + zap.ascan.status
        time.sleep(5)

    print 'Generating reports:'
    with open(reportDir + '\\XMLReport_' + sessionNames[i] + '.xml', 'w') as text_file:
        text_file.write(zap.core.xmlreport)
        text_file.close()

    i = i + 1

print 'Done!'
