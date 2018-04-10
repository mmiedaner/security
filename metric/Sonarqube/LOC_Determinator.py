import httplib
import json
import argparse
import sys
import pandas

mainURL = None
excel = None

def make_apicall(connection, method, apistring):
    connection.request(method, apistring)
    resp = connection.getresponse()
    data = json.load(resp)
    return data

def get_lines_of_code_per_project(connection):
    service_answer = make_apicall(connection, "GET", "/sonar/api/resources?metrics=ncloc,coverage")
    lines_of_code_dictionary = []

    project_name = ""
    lines_of_code = ""
    project_key = ""
    for service_item in service_answer:
        item = {}
        if service_item['name']:
            project_name = service_item['name']

        if service_item['key']:
            project_key = service_item['key']

        if 'msr' in service_item.keys():
            measures = service_item['msr']

            for measure in measures:
                if 'key' in measure.keys():
                    if measure['key'] == "ncloc":
                        lines_of_code = measure['val']

        item = {'project_name': project_name, 'lines_of_code': lines_of_code, 'project_key': project_key}
        lines_of_code_dictionary.append(item)

    return lines_of_code_dictionary

def parser_arguments():
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarqube based on repositories of rules.')
    parser.add_argument('--excel', metavar='excel', help='name of excel file')
    parser.add_argument('--baseurl', metavar='baseurl', help='base url of sonar')

    args = parser.parse_args()
    global mainURL
    if args.baseurl:
        mainURL = args.baseurl

    global excel
    if args.excel:
        excel = args.excel

## main routine
parser_arguments()
conn = httplib.HTTPSConnection(mainURL)
locDict = get_lines_of_code_per_project(conn)
df2 = pandas.DataFrame(locDict, columns=['project_name', 'lines_of_code', 'project_key'])
file_name_parts = excel.split('.')
df2.to_excel(file_name_parts[0] + "_loc." + file_name_parts[1], sheet_name='sheet1', index=False)
