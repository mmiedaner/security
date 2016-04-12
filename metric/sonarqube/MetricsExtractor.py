import httplib
import json
import argparse
import sys

import pandas


fileName = None
repo = None
language = None
mainURL = None
separator = None
tags = None
excel = None
date_separator = None


def write_statusmessage(messageid, i, maximum):
    sys.stdout.write('\r Collecting issues for key: ' + messageid + ' - page ' + str(i) + ' of ' + str(maximum))
    sys.stdout.flush()
    return


def make_apicall(connection, method, apistring):
    connection.request(method, apistring)
    resp = connection.getresponse()
    data = json.load(resp)
    return data


def get_rulekeys_by_repo(connection):
    url = '/sonar/api/profiles?language=' + language
    service_answer = make_apicall(connection, "GET", url)
    squid = set()
    for profile in service_answer:
        if 'rules' in profile:
            for rule in profile['rules']:
                for repos in repo:
                    if rule['repo'] == repos:
                        key_string = repos + ":" + rule['key']
                        squid.add(key_string)
    return squid


def extract_keys_from_response(service_answer, squid):
    if 'rules' in service_answer:
        rules = service_answer['rules']
        for rule in rules:
            if 'key' in rule:
                squid.add(rule['key'])
    return squid


def get_rulekeys_by_tag(connection):
    tag_string = ""
    for tag in tags:
        tag_string += str(tag) + ","
    url = '/sonar/api/rules/search?language=' + language + '&tags=' + tag_string
    service_answer = make_apicall(connection, "GET", url)

    squid = set()
    squid = extract_keys_from_response(service_answer, squid)

    if 'total' in service_answer and service_answer['total'] > 1:
        p = 1
        while p < service_answer['total']:
            p += 1
            url2 = url + "&p=" + str(p)
            service_answer2 = make_apicall(connection, "GET", url2)
            squid = extract_keys_from_response(service_answer2, squid)
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
    global fileName
    if args.out:
        fileName = args.out

    global repo
    if args.repo:
        repo = args.repo

    global language
    if args.lang:
        language = args.lang

    global mainURL
    if args.baseurl:
        mainURL = args.baseurl

    global separator
    if args.separator:
        separator = args.separator
    else:
        separator = "\t"

    global tags
    if args.tags:
        tags = args.tags

    global excel
    if args.excel:
        excel = args.excel

    global date_separator
    if args.date_separator:
        date_separator = args.date_separator


def validate_args(arguments):
    if arguments.tags and arguments.repo:
        print 'You need to specify either a repositories or tags to search for issues'
        exit(1)

    if not arguments.tags and not arguments.repo:
        print 'You need to specify either a repositories or tags to search for issues'
        exit(1)


def parse_commandline_paramters():
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarquebe based on repositories of rules.')


    parser.add_argument('--repo', metavar='repo', help='name of repository to query', nargs='+')
    parser.add_argument('--lang', metavar='lang', help='progamming language used in projects')
    parser.add_argument('--baseurl', metavar='burl', help='base url of sonarqube server')
    parser.add_argument('--separator', metavar='sepa', help='separator used - defaults to tab')
    parser.add_argument('--tags', metavar='tags', help='either specify tags or a repository to search rules', nargs='+')
    parser.add_argument('--date_separator', metavar="splitdate",
                        help="Separator used to split dates, default = no split")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--out', metavar='file', help='file to write output to')
    group.add_argument('--excel',metavar='excel', help='Write output as excel with provided filename')
    args = parser.parse_args()
    validate_args(args)
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
                elif (element == 'creationDate' or element == 'updateDate') and date_separator is not None:
                    element_string = str(issue[str(element)])
                    date_string = element_string.split(date_separator)
                    body += date_string[0].title() + separator + date_string[1].title() + separator
                else:
                    body += str(issue[str(element)]) + separator

            else:
                body += " " + separator
        except UnicodeEncodeError:
            body += " " + separator
    body += " \n"
    if excel is None:
        return body
    else:
        result = list(body.split(separator))
        return result


def write_to_file(file_to_write_to, issuelist):
    for issue in issuelist:
        line_item = generate_lineitem(issue)
        file_to_write_to.write(line_item)

##
## main routine
##
parse_commandline_paramters()
conn = httplib.HTTPSConnection(mainURL)
if repo is not None:
    result = get_rulekeys_by_repo(conn)
else:
    result = get_rulekeys_by_tag(conn)
print str(len(result)) + ' Rules to check. \n'

output_file = None
if excel is None:
    try:
        output_file = open(fileName, "wb+")
    except IOError:
        print 'Could not open file - exiting'
        exit(0)

header = ""
if date_separator is None:
    header = 'status' + separator + 'line' + separator + 'creationDate' + separator + 'fUpdateAge' + separator \
             + 'severity' + separator + 'componentName' + separator + 'component' + separator + 'rule' + separator \
             + 'project' + separator + 'updateDate' + separator + 'key' + separator + 'message' + separator + 'debt' \
             + separator + 'componentId\n'
else:
    header = 'status' + separator + 'line' + separator + 'creationDate' + separator + 'creationTime' + separator + \
             'fUpdateAge' + separator + 'severity' + separator + 'componentName' + separator + 'component' + separator \
             + 'rule' + separator + 'project' + separator + 'updateDate' + separator + 'updateTime' + separator + 'key' \
             + separator + 'message' + separator + 'debt' + separator + 'componentId\n'

lineitem_list = []

if excel is None:
    output_file.write(header)

for key in result:
    issues = get_issues_for_squid(conn, key)
    if issues is not None:
        if excel is None:
            write_to_file(output_file, issues)
        else:
            for issue in issues:
                lineitem_list.append(generate_lineitem(issue))
                ## TODO handle memory overflow

if excel is None:
    output_file.close()
else:
    columns = header.split(separator)
    columns.append('')
    if len(lineitem_list) != 0:
        df = pandas.DataFrame(lineitem_list, columns=columns)
        df.to_excel(excel, sheet_name='sheet1', index=False)
        ## TODO handle number of rows exceeded

print "\n Done!"
exit(0)
