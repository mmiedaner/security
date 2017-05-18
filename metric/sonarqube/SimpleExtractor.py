import httplib
import json
import argparse
import pandas
import datetime
import numpy


baseurl = None
iName = None
rName = None
excel = None
debug = None


def log_message(message):
    if debug:
        print message


def make_http_call(connection, method, api_string):
    connection.request(method, api_string)
    resp = connection.getresponse()
    response = json.load(resp)
    return response


def make_apicall(connection, method, api_string, key_of_rule):
    response_data = make_http_call(connection, method, api_string)
    dat = None
    runs = 0
    if 'total' in response_data:
        runs = response_data['total'] / response_data['ps'] + 1
        if debug:
            log_message("Will do " + str(runs) + " runs.")
    i = 2

    if key_of_rule is not None and key_of_rule in response_data:
        dat = response_data[key_of_rule]

    while i <= runs:
        api_string = apistring_rules + "?p=" + str(i)
        log_message(api_string)
        i += 1
        response_data = make_http_call(connection, method, api_string)
        if key_of_rule is not None and key_of_rule in response_data:
            dat.extend(response_data[key_of_rule])

    return dat


def parse_commandline_paramters():
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarquebe based on repositories of rules.')

    parser.add_argument('--baseurl', metavar='burl', help='base url of sonarqube server')
    parser.add_argument('--install_name', metavar='iName', help='context path element specific for your installation')
    parser.add_argument('--rule_name', metavar='rName', help='name of ruleset to query', nargs='+')
    parser.add_argument('--out', metavar='out', help='name of output file')
    parser.add_argument('--debug', metavar='debug', help='enable debug output')

    args = parser.parse_args()

    if args.baseurl:
        global baseurl
        baseurl = args.baseurl

    if args.install_name:
        global iName
        iName = args.install_name

    if args.rule_name:
        global rName
        rName = args.rule_name

    if args.out:
        global excel
        excel = args.out

    if args.debug:
        global debug
        debug = True


def add_key_to_set(data_set, key_part, keys_of_rules):
    for rule in data_set:
        rule_key = rule['key']
        if key_part in rule_key:
            keys_of_rules.add(rule['key'])


def calculate_delta(datum):
    date_string = datum.split("-")
    d0 = datetime.date(int(date_string[0]), int(date_string[1]), int(date_string[2].split('T')[0]))
    d1 = datetime.date.today()
    delta = d1 - d0
    return delta.days


def generate_lineitem(issue_list, header_list):
    lineitem_list = []

    for issue in issue_list:
        result = []

        for head in header_list:
            if head in issue and head != 'delta':
                result.append(issue[head])

            elif head == 'delta' and "creationDate" in issue:
                datum = str(issue['creationDate']).split("T")[0]
                result.append(calculate_delta(datum))
            elif head == 'count':
                result.append(1)
            else:
                result.append("")

        lineitem_list.append(result)

    return lineitem_list


def create_pivot_analysis(df_togroup, column_name_to_group, helper_column, set_of_bins, set_of_labels):
    labels_to_use = numpy.asarray(set_of_labels)
    bins_to_use = numpy.asarray(set_of_bins)
    df_togroup[helper_column] = pandas.cut(df_togroup[column_name_to_group], bins=bins_to_use, labels=False)
    df_togroup['result1'] = labels_to_use[df_togroup[helper_column]]
    return df_togroup.groupby(df_togroup[helper_column]).sum()


def group_by_severity(dataframe):
    major = 0
    minor = 0
    blocker = 0
    critical = 0
    info = 0

    for index, row in dataframe.iterrows():
        sev = row['severity']
        if sev == 'BLOCKER':
            blocker += 1
        elif sev == 'CRITICAL':
            critical += 1
        elif sev == 'MAJOR':
            major += 1
        elif sev == 'MINOR':
            minor += 1
        elif sev == 'INFO':
            info += 1
        else:
            print "Could not determine severity"

    result_data = {'BLOCKER': blocker, 'CRITICAL': critical, 'MAJOR': major, 'MINOR': minor, 'INFO': info}
    df_sev = pandas.DataFrame(result_data, index={1})
    log_message(df_sev)
    return df_sev


def dfs_tabs(df_list, sheet_list, file_name):
    writer = pandas.ExcelWriter(file_name)
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
    writer.save()


## Main Routine
parse_commandline_paramters()
apistring_issues = "/" + str(iName) + "/api/issues/search?resolved=false&types=VULNERABILITY"
apistring_rules = "/" + str(iName) + "/api/rules/search"

conn = httplib.HTTPSConnection(baseurl)
data = make_apicall(conn, "GET", apistring_rules, 'rules')

keys = set()
for ru in rName:
    add_key_to_set(data, str(ru), keys)

rules_string = "rules "
for key in keys:
    rules_string += str(key) + ","
apistring_issues += "&" + rules_string[:-1]

issues = make_apicall(conn, "GET", apistring_issues, "issues")
header = ['status', 'line', 'creationDate', 'severity', 'component', 'rule', 'project', 'message', 'delta', 'count']
line_items = generate_lineitem(issues, header)

if len(line_items) is not 0:
    df = pandas.DataFrame(line_items, columns=header)
    bins = numpy.arange(0, 625, 125)
    labels = ['bis125', 'bis250', 'bis375', 'bis500', 'bis650', 'gr650']
    df1 = create_pivot_analysis(df, 'delta', 'result1', bins, labels)

    count_bins = ['BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'INFO']
    df2 = group_by_severity(df)

    dfs = [df, df1, df2]
    sheets = ['data', 'daysOpen', 'severity']

    dfs_tabs(dfs, sheets, excel)

else:
    print "no data received - exit now!"
