import time
import os
import json
import sys
import argparse
from datetime import date
from zapv2 import ZAPv2

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
            targeturl = {'url': url, 'respider': 'false', 'sessionName': session_name, 'scan': 'true'}
            targets.append(targeturl)
            i += 1

        config = {'falsePositive': [], 'reportDir': '..', 'target': targets, 'sessionPath': '..'}
    return config


#set up environment for scanning
def setup_env(config):
    if not os.path.exists(config['sessionPath']):
        os.makedirs(config['sessionPath'])

    if not os.path.exists(config['reportDir']):
        os.makedirs(config['reportDir'])
    return


def spider(url):
    print 'Starting Spider'
    zap.spider.scan(url)
    time.sleep(2)
    while int(zap.spider.status()) < 100:
        sys.stdout.write("\rSpider progress: " + zap.spider.status + "%")
        sys.stdout.flush()
        time.sleep(2)
    print '\nSpider completed'
    time.sleep(5)


def scan(url):
    print 'Scanning target: %s' % url
    zap.ascan.scan(url)
    while int(zap.ascan.status()) < 100:
        sys.stdout.write("\rScan status: " + zap.ascan.status + "%")
        sys.stdout.flush()
        time.sleep(5)
    print '\nScan completed.'


# do the actual scan
def do_scan(target_data):
    print 'Creating session %s' % target_data["sessionName"]
    zap.core.new_session(configuration["sessionPath"] + '\\' + target_data["sessionName"])

    print 'Accessing target %s' % target_data["url"]
    zap.urlopen(target_data["url"])
    time.sleep(2)

    spider(target['url'])

    if target['scan'] and target['scan'] is True:
        scan(target['url'])

    if target['respider'] and target['respider'] is True:
        spider(target['url'])

    return


def generate_report(target_data):
    print 'Generating reports:'
    report = ""
    extension = ""

    if configuration['reportType'] == "HTML":
        report = zap._request_other(zap.base_other + 'core/other/htmlreport/', {'apikey': None})
        extension = ".html"
    else:
        report = zap.core.xmlreport
        extension = ".xml"

    with open(configuration["reportDir"] + '\\Report_' + target_data["sessionName"] + extension, 'w') as text_file:
        text_file.write(report)
        text_file.close()

    print 'Done!'


def parse_args():
    parser = argparse.ArgumentParser(description='Start ZAP and scan web apps.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--config', metavar='config', help='config file to use')
    group.add_argument('--urls', metavar='url', help='space separated list of urls to scan', nargs='+')
    parser.add_argument('--setssion', metavar='session', help='session file to start from')

    global args
    args = parser.parse_args()


def handle_false_positivies(alerts):
    return_list = []
    for alert in alerts:
        false_positive_list = configuration['falsePositive']

        for fp in false_positive_list:
            match = 0
            crit = 0
            if 'url' in fp and fp['url'] is not None:
                crit += 1
                if 'url' in alert and alert['url'] == fp['url']:
                    match += 1

            if 'param' in fp and fp['param'] is not None:
                crit += 1
                if 'param' in alert and alert['param'] == fp['param']:
                    match += 1

            if 'evidence' in fp and fp['evidence'] is not None:
                crit += 1
                if 'evidence' in alert and alert['evidence'] == fp['evidence']:
                    match += 1

            if 'alert' in fp and fp['alert'] is not None:
                crit += 1
                if 'alert' in alert and alert['alert'] == fp['alert']:
                    match += 1

            if match != crit:
                return_list.append(alert)

    return return_list


def generate_custom_report(target_data):
    alerts = zap.core.alerts()

    if configuration['falsePositive']:
        clean_alerts = handle_false_positivies(alerts)
    else:
        clean_alerts = alerts

    report = '<html> <style> table { background-color: #e8e8e8; width: 100%; } .small { width: 20%; } </style> ' \
             '<body> <h1 style="text-align: center;"> Custom Zap Report </h1>'

    for al in clean_alerts:
        report_item = "<table>"
        if 'alert' in al and al['alert'] is not None:
            report_item += '<tr><td class="small"><h3>Alert:</h3></td><td>' + al['alert'] + '</td></tr>'
        if 'risk' in al and al['risk'] is not None:
            report_item += '<tr><td class="small"><h3>Risk:</h3></td><td>' + al['risk'] + '</td></tr>'
        if 'url' in al and al['url'] is not None:
            report_item += '<tr><td class="small"><h3>URL</h3></td><td>' + al['url'] + '</td></tr>'
        if 'param' in al and al['param'] is not None:
            report_item += '<tr><td class="small"><h3>Parameter</h3></td><td>' + al['param'] + '</td></tr>'
        if 'attack' in al and al['attack'] is not None:
            report_item += '<tr><td class="small"><h3>Attack</h3></td><td>' + al['attack'] + '</td></tr>'
        if 'evidence' in al and al['evidence'] is not None:
            report_item += '<tr><td class="small"><h3>Evidence</h3></td><td>' + al['evidence'] + '</td></tr>'
        if 'description' in al and al['description'] is not None:
            report_item += '<tr><td class="small"><h3>Description</h3></td><td>' + al['description'] + '</td></tr>'
        if 'solution' in al and al['solution'] is not None:
            report_item += '<tr><td class="small"><h3>Solution</h3></td><td>' + al['solution'] + '</td></tr>'
        report_item += '</table> <p></p> <p></p> '
        report += report_item

    report += '</body> </html>'
    with open(configuration["reportDir"] + '\\Report_' + target_data["sessionName"] + ".html", 'w') as text_file:
        text_file.write(report.encode("utf8"))
        text_file.close()

## Main
parse_args()
print 'Loading environment'
configuration = load_config()
setup_env(configuration)

print 'Initializing ZAPClient'
if 'http-proxy' in configuration and configuration['http-proxy'] != "" and 'https-proxy' in configuration and \
                configuration['https-proxy'] != "":
    proxy_data = {'http': configuration['http-proxy'], 'https': configuration['https-proxy']}
    zap = ZAPv2(proxies={'http': 'http://10.198.37.50:1171', 'https': 'http://10.198.37.50:1171'})
else:
    zap = ZAPv2()

if args.session != None:
    print "loading session"
    zap.core.load_session(args.session)
    sites = zap.core.sites
    url = sites[len(sites)-1]
    print "scanning url: " + url
    scan(url)
    report = zap._request_other(zap.base_other + 'core/other/htmlreport/', {'apikey': None})
    extension = ".html"
    with open(args.session + extension, 'w') as text_file:
        text_file.write(report)
        text_file.close()
    print "Done writing report"
    exit(0)

# Loop over all targets, spider them, scan them and generate reports
for target in configuration["target"]:
    if 'selenium' in target:
        print 'Starting SE-Script before scanning'
        os.system(target["selenium"])

    do_scan(target)

    if configuration['reportType'] == "Custom":
        generate_custom_report(target)
    else:
        generate_report(target)
