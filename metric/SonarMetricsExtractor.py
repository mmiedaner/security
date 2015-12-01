import httplib
import json
import argparse
import sys


def writeStatusMsg(id, i, maximum):
    sys.stdout.write('\r Collecting issues for key: ' + id + ' - page ' + str(i) + ' of ' + str(maximum))
    sys.stdout.flush()
    return


def makeApiCall(connection, method, apiString):
    connection.request(method, apiString)
    resp = connection.getresponse()
    data = json.load(resp)
    return data


def getRuleKeys(connection):
    url = '/sonar/api/profiles?language=' + language
    result = makeApiCall(connection, "GET", url)
    squid = []
    for profile in result:
        if 'rules' in profile:
            for rule in profile['rules']:
                for repos in repo:
                    if rule['repo'] == repos:
                        squid.append(rule['key'])
    return squid


def getIssuesForSquid(connection, id):
    url = "/sonar/api/issues/search?squid=" + id + "&pageSize=-1"
    result = makeApiCall(connection, "GET", url)
    issueList = []
    if 'issues' in result:
        for issue in result['issues']:
            issueList.append(issue)

    if 'maxResultsReached' in result and result['maxResultsReached']:
        paging = result['paging']
        i = paging['pageIndex']
        while i < paging['pages']:
            i += 1
            writeStatusMsg(id, i, paging['pages'])
            result2 = makeApiCall(connection, "GET", url + "&pageIndex=" + str(i))
            if 'issues' in result2:
                for issue in result2['issues']:
                    issueList.append(issue)

    if len(issueList) > 0:
        return issueList

    return "nix"


def mapArgsToGloablVars(args):
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


def parseCommandlineParamters():
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarquebe based on repositories of rules.')
    parser.add_argument('--out', metavar='file', help='file to write output to')
    parser.add_argument('--repo', metavar='repo', help='name of repository to query', nargs='+')
    parser.add_argument('--lang', metavar='lang', help='progamming language used in projects')
    parser.add_argument('--baseurl', metavar='burl', help='base url of sonarqube server')
    args = parser.parse_args()
    mapArgsToGloablVars(args)


def generateLineItem(issue):
    lineItemElements = ["status", "line", "creationDate", "fUpdateAge", "severity", "component",
                        "rule", "project", "updateDate", "key", "message", "debt", "componentId"]

    body = ""
    for element in lineItemElements:
        try:
            if str(element) in issue:
                body += str(issue[str(element)]) + "\t"
            else:
                body += " \t"
        except (UnicodeEncodeError):
            body += " \t"
    body += " \n"
    return body


def writeToFile(fileName, issueList):
    print "Persisting: ", len(issueList), " issues now."
    f = open(fileName, "wb+")
    header = 'status\tline\tcreationDate\tfUpdateAge\tseverity\tcomponent\trule\tproject\tupdateDate\tkey\tmessage\tdebt\tcomponentId\n'
    f.write(header)

    for issue in issueList:
        lineItem = generateLineItem(issue)
        f.write(lineItem)

        # does not work - number of rows exceeded ;)
        # df = pandas.DataFrame(issueList)
        # df.to_excel(fileName, sheet_name='sheet1', index=False)

##
## main routine
##
parseCommandlineParamters()
conn = httplib.HTTPSConnection(mainURL)
result = getRuleKeys(conn)
print str(len(result)) + ' Rules to check. \n'

issueList = []
for key in result:
    issues = getIssuesForSquid(conn, key)
    if issues != 'nix':
        for issue in issues:
            issueList.append(issue)

writeToFile(fileName, issueList)
print "Done! - Collected " + str(len(issueList)) + " issues."
exit(0)
