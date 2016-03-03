import time
import os
import json
from zapv2 import ZAPv2
import sys
import argparse
from datetime import date

# This is a simple ZAP Wrapper in Python for scanning multible WebApplications in a row
# author: markusmiedaner@gmail.com
args = None


# load config / profile from file or commandline
def load_config():
    if args.config and args.config is not None:
        with open(args.config) as config_file:
            config = json.load(config_file)

    else:
        targets = []
        i = 0
        for url in args.urls:
            session_name = "new_session_" + str(date.today()) + "_" + str(i)
            targeturl = {'url': url, 'respider': 0, 'sessionName': session_name}
            targets.append(targeturl)
            i += 1

        config = {'falsePositive': [], 'reportDir': '..', 'target': targets, 'raiseAlertItem': [], 'sessionPath': '..',
                  'lowerAlertItem': []}

    return config


#set up environment for scanning
def setup_env(config):
    if not os.path.exists(config['sessionPath']):
        os.makedirs(config['sessionPath'])

    if not os.path.exists(config['reportDir']):
        os.makedirs(config['reportDir'])
    return


# do the actual scan
def do_scan(target_data):
    print 'Creating session %s' % target_data["sessionName"]
    zap.core.new_session(configuration["sessionPath"] + '\\' + target_data["sessionName"])

    print 'Accessing target %s' % target_data["url"]
    zap.urlopen(target_data["url"])
    time.sleep(2)

    print 'Starting Spider'
    zap.spider.scan(target_data["url"])
    time.sleep(2)

    while int(zap.spider.status) < 100:
        sys.stdout.write("\rSpider progress: " + zap.spider.status + "%")
        sys.stdout.flush()
        time.sleep(2)

    print '\nSpider completed'
    time.sleep(5)

    print 'Scanning target: %s' % target["url"]
    zap.ascan.scan(target["url"])

    while int(zap.ascan.status) < 100:
        sys.stdout.write("\rScan status: " + zap.ascan.status + "%")
        sys.stdout.flush()
        time.sleep(5)

    print '\nScan completed.'
    return


def generate_report(target_data):
    print 'Generating reports:'
    with open(configuration["reportDir"] + '\\XMLReport_' + target_data["sessionName"] + '.xml', 'w') as text_file:
        text_file.write(zap.core.xmlreport)
        text_file.close()

    print 'Done!'
    return


def parse_args():
    parser = argparse.ArgumentParser(description='Start ZAP and scan web apps.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--config', metavar='config', help='config file to use')
    group.add_argument('--urls', metavar='url', help='space separated list of urls to scan', nargs='+')

    global args
    args = parser.parse_args()


print 'Initializing ZAPClient'
zap = ZAPv2()

parse_args()

print 'Loading environment'
configuration = load_config()
setup_env(configuration)


# Loop over all targets, spider them, scan them and generate reports
for target in configuration["target"]:
    if 'selenium' in target:
        print 'Starting SE-Script before scanning'
        os.system(target["selenium"])

    do_scan(target)
    generate_report(target)
