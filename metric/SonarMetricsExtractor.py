import httplib
import json
import argparse
import sys


def write_statusmessage(messageid, i, maximum):
    sys.stdout.write('\r Collecting issues for key: ' + messageid + ' - page ' + str(i) + ' of ' + str(maximum))
    sys.stdout.flush()
    return


def make_apicall(connection, method, apistring):
    connection.request(method, apistring)
    resp = connection.getresponse()
    data = json.load(resp)
    return data


def get_rulekeys(connection):
    url = '/sonar/api/profiles?language=' + language
    service_answer = make_apicall(connection, "GET", url)
    squid = []
    for profile in service_answer:
        if 'rules' in profile:
            for rule in profile['rules']:
                for repos in repo:
                    if rule['repo'] == repos:
                        squid.append(repos + ":" + rule['key'])
    return squid


def get_issues_for_squid(connection, squid_id):
    url = "/sonar/api/issues/search?rules=" + squid_id + "&pageSize=-1"
    service_answer = make_apicall(connection, "GET", url)
    issuelist = []
    if 'issues' in service_answer:
        for issue in service_answer['issues']:
            issuelist.append(issue)

    if 'maxResultsReached' in service_answer and service_answer['maxResultsReached']:
        paging = service_answer['paging']
        i = paging['pageIndex']
        while i < paging['pages']:
            i += 1
            write_statusmessage(squid_id, i, paging['pages'])
            result2 = make_apicall(connection, "GET", url + "&pageIndex=" + str(i))
            if 'issues' in result2:
                for issue in result2['issues']:
                    issuelist.append(issue)

    if len(issuelist) > 0:
        return issuelist

    return None


def map_args_to_global_vars(args):
    if args.out:
        global fileName
        fileName = args.out

    if args.repo:
        global repo
        repo = args.repo

    if args.lang:
        global language
        language = args.lang

    if args.baseurl:
        global mainURL
        mainURL = args.baseurl

    global separator
    if args.separator:
        separator = args.separator
    else:
        separator = "\t"


def parse_commandline_paramters():
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarquebe based on repositories of rules.')
    parser.add_argument('--out', metavar='file', help='file to write output to')
    parser.add_argument('--repo', metavar='repo', help='name of repository to query', nargs='+')
    parser.add_argument('--lang', metavar='lang', help='progamming language used in projects')
    parser.add_argument('--baseurl', metavar='burl', help='base url of sonarqube server')
    parser.add_argument('--separator', metavar='sepa', help='separator used - defaults to tab')
    args = parser.parse_args()
    map_args_to_global_vars(args)


def generate_lineitem(issue):
    lineitemelements = ["status", "line", "creationDate", "fUpdateAge", "severity", "component",
                        "rule", "project", "updateDate", "key", "message", "debt", "componentId"]

    body = ""
    for element in lineitemelements:
        try:
            if str(element) in issue:

                if element == 'component':
                    component_string = str(issue[str(element)])
                    components = component_string.split(":")
                    body += components[1].title() + separator + component_string + separator
                else:
                    body += str(issue[str(element)]) + separator

            else:
                body += " " + separator
        except UnicodeEncodeError:
            body += " " + separator
    body += " \n"
    return body


def write_to_file(file_to_write_to, issuelist):
    for issue in issuelist:
        line_item = generate_lineitem(issue)
        file_to_write_to.write(line_item)

##
## main routine
##
parse_commandline_paramters()
conn = httplib.HTTPSConnection(mainURL)
result = get_rulekeys(conn)
print str(len(result)) + ' Rules to check. \n'

output_file = None
try:
    output_file = open(fileName, "wb+")
except IOError:
    print 'Could not open file - exiting'
    exit(0)

header = 'status' + separator + 'line' + separator + 'creationDate' + separator + 'fUpdateAge' + separator \
         + 'severity' + separator + 'componentName' + separator + 'component' + separator + 'rule' + separator \
         + 'project' + separator + 'updateDate' + separator + 'key' + separator + 'message' + separator + 'debt' \
         + separator + 'componentId\n'
output_file.write(header)

for key in result:
    issues = get_issues_for_squid(conn, key)
    if issues is not None:
        write_to_file(output_file, issues)

output_file.close()
print "\n Done!"
exit(0)
