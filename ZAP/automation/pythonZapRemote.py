import time
import os
import json
from pprint import pprint
from zapv2 import ZAPv2


# This is a simple ZAP Wrapper in Python for scanning multible WebApplications in a row
# author: markusmiedaner@gmail.com


# load config / profile from file
def loadConfig(profileName):
    with open(profileName) as config_file:
        config = json.load(config_file)
        return config

#set up environment for scanning
def setUpEnv(configuration):
    if not os.path.exists(configuration['sessionPath']):
        os.makedirs(configuration['sessionPath'])

    if not os.path.exists(configuration['reportDir']):
        os.makedirs(configuration['reportDir'])
    return

# do the actual scan
def doScan(target):
    print 'Creating session %s' % target["sessionName"]
    zap.core.new_session(configuration["sessionPath"] + '\\' + target["sessionName"])

    print 'Accessing target %s' % target["url"]
    zap.urlopen(target["url"])
    time.sleep(2)

    print 'staring spider'
    zap.spider.scan(target["url"])
    time.sleep(2)

    while (int(zap.spider.status) < 100):
        print 'Spider progress %:' + zap.spider.status
        time.sleep(2)

    print 'Spider completed'
    time.sleep(5)

    print 'Scanning target: %s' % target["url"]
    zap.ascan.scan(target["url"])

    while (int(zap.ascan.status) < 100):
        print 'Scan progress %:' + zap.ascan.status
        time.sleep(5)
    return
	
def generateReport(target):
    print 'Generating reports:'
    with open(configuration["reportDir"] + '\\XMLReport_' + target["sessionName"] + '.xml', 'w') as text_file:
        text_file.write(zap.core.xmlreport)
        text_file.close()

    print 'Done!'
    return


print 'Initializing ZAPClient'
zap = ZAPv2()

print 'loading environment'
# setting environmental variables from config file
configuration = loadConfig('config.json')
setUpEnv(configuration)


# Loop over all targets, spider them, scan them and generate reports
for target in configuration["target"]:
	print 'Scanning target: ' + target["url"]
	if target["selenium"] is not '':
		print 'Starting SE-Script before scanning'
		os.system(target["selenium"])

	doScan(target)
	generateReport(target)
