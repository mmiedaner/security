import argparse
import datetime
import json

import pandas

from DataAnalyser import DataAnalyser
from ExcelAdaptor import ExcelAdaptor
from Logger import Logger
from SonarAPIClient import SonarAPIClient

file_name = None
repo = None
language = None
main_url = None
separator = None
tags = None
excel = None
date_separator = None
install_name = None
analyze = None
configuration = None


def generate_lineitemlist(list_of_issues):
    """
    Generates lineitemlist from a list of issues
    :param list_of_issues: - List to be operated on
    :return: lineitemlist
    """
    list_to_return = []
    for issue in list_of_issues:
        list_to_return.append(generate_lineitem(issue))
    return list_to_return


def map_args_to_global_vars(args):
    """
    maps args provided to global variables
    :param args: args to map
    :return: NONE
    """
    global file_name
    if args.out:
        file_name = args.out

    global repo
    if args.repo:
        repo = args.repo

    global language
    if args.lang:
        language = args.lang

    global main_url
    if args.baseurl:
        main_url = args.baseurl

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

    global install_name
    if args.install_name:
        install_name = args.install_name
    else:
        install_name = '/sonar'

    global analyze
    if args.analyze == "True" or args.analyze is True:
        analyze = True

    global configuration
    if args.config:
        configuration = json.load(open(args.config))


def validate_args(arguments):
    """
    validate commandline arguments
    :param arguments:
    :return: NONE
    """
    if arguments.tags and arguments.repo:
        print 'You need to specify either a repositories or tags to search for issues'
        exit(1)

    if not arguments.tags and not arguments.repo:
        print 'You need to specify either a repositories or tags to search for issues'
        exit(1)


def parse_commandline_paramters():
    """
    Parse commandline arguments
    :return: NONE
    """
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarquebe based on repositories of rules.')

    parser.add_argument('--repo', metavar='repo', help='name of repository to query', nargs='+')
    parser.add_argument('--lang', metavar='lang', help='progamming language used in projects', default="java")
    parser.add_argument('--baseurl', metavar='burl', help='base url of sonarqube server')
    parser.add_argument('--separator', metavar='sepa', help='separator used - defaults to tab')
    parser.add_argument('--tags', metavar='tags', help='either specify tags or a repository to search rules', nargs='+')
    parser.add_argument('--date_separator', metavar="splitdate",
                        help="Separator used to split dates, default = no split")
    parser.add_argument('--install_name', metavar='install_name', help='name sonar installation / context path')
    parser.add_argument('--analyze', metavar="analyze",
                        help='true or flase depending if analysis of data should be performed or not', default=False)
    parser.add_argument('--config', metavar='config', help='path to config file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--out', metavar='file', help='file to write output to')
    group.add_argument('--excel', metavar='excel', help='Write output as excel with provided filename')
    args = parser.parse_args()
    validate_args(args)
    map_args_to_global_vars(args)


def generate_lineitem(issue):
    """
    Generates Lineitem based on issue
    :param issue: Issue to create lineitem from
    :return: lineitem as list of lists
    """
    lineitemelements = ["status", "line", "creationDate", "fUpdateAge", "severity", "component",
                        "rule", "project", "updateDate", "key", "message", "debt", "componentId", "tags"]

    body = ""
    for element in lineitemelements:
        try:
            if str(element) in issue:

                if element == 'component':
                    component_string = str(issue[str(element)])
                    components = component_string.split(":")
                    if len(components) >= 2:
                        body += components[1].title() + separator + component_string + separator
                    else:
                        body += " " + separator + component_string + separator
                elif (element == 'creationDate' or element == 'updateDate') and date_separator is not None:
                    element_string = str(issue[str(element)])
                    date_string = element_string.split(date_separator)
                    body += date_string[0].title() + separator + date_string[1].title() + separator
                elif element == 'tags':
                    if issue[element]:
                        body += " ".join(issue[str(element)]) + separator
                    else:
                        body += " " + separator
                else:
                    body += str(issue[str(element)]) + separator
            else:
                body += " " + separator
        except UnicodeEncodeError:
            body += " " + separator

    body += str(calculate_delta(issue['creationDate'])) + separator + " \n"
    if excel is None:
        return body
    else:
        return list(body.split(separator))


def calculate_delta(datum):
    """
    Calculate delta of days between date given and today.
    :param datum: date given
    :return: amount of days between date given and today
    """
    date_string = datum.split("-")
    d0 = datetime.date(int(date_string[0]), int(date_string[1]), int(date_string[2].split('T')[0]))
    d1 = datetime.date.today()
    delta = d1 - d0
    return delta.days


# main routine
parse_commandline_paramters()

logger = Logger("debug", "SonarMetricsExtractor")
api_client = SonarAPIClient(main_url)
logger.log("debug", "initialized all components")

issues_list = api_client.search_issues(install_name, 'VULNERABILITY', 'OPEN,REOPENED,CONFIRMED', None)
logger.log("debug", "collected: " + str(len(issues_list)) + " from Sonar")
lineitem_list = generate_lineitemlist(issues_list)
logger.log("debug", "generated lineitemlist for open issues")

columns = ["status", "line", "creationDate", "fUpdateAge", "", "severity", "component", "file", "rule", "project",
           "updateDate", "updateDateTime", "key", "message", "a", "b", "tags", "delta", "c"]

issues_list2 = api_client.search_issues(install_name, 'VULNERABILITY', None, 'WONTFIX')
lineitem_list2 = generate_lineitemlist(issues_list2)
logger.log("debug", "generated lineitemlisnt for wontfix issues")
df4 = pandas.DataFrame(lineitem_list2, columns=columns)

excel_adaptor = ExcelAdaptor()

data_analyser = DataAnalyser()

df_separator = pandas.DataFrame(["--", "--"], columns=['SEPERATOR-WONT-FIX->'])

df = df2 = df3 = df_wontfix = df_wontfix_analysis = df_wontfix_applications = None

if analyze:
    injection_filter = configuration['cwe_filters']['injection_cwes']
    iam_filter = configuration['cwe_filters']['iam_cwes']

    if len(lineitem_list) != 0:
        logger.log("debug", "analysing open issues")
        df = pandas.DataFrame(lineitem_list, columns=columns)
        df3 = data_analyser.generate_dependency_checker_report(df)
        df3['CVSS'] = pandas.to_numeric(df3['CVSS'])

        cwe_injection_app = data_analyser.analyse_by_applications(df3[df3['CVSS'] >= float(configuration['cvss_filter'])], configuration['applications'], injection_filter)
        cwe_iam_app = data_analyser.analyse_by_applications(df3[df3['CVSS'] >= float(configuration['cvss_filter'])], configuration['applications'], iam_filter)
        df_inject_app = pandas.DataFrame(cwe_injection_app, columns=["App Inject", "Count"])
        df_iam_app = pandas.DataFrame(cwe_iam_app, columns=["App IAM", "Count"])
        df_applications = pandas.concat([df_inject_app, df_iam_app], axis=1)

        df2 = data_analyser.analyse(df, df3, tags)

    if len(df4) != 0 and analyze:
        logger.log("debug", "analysing wontfix issues")
        df_wontfix = data_analyser.generate_dependency_checker_report(df4)
        df_wontfix_analysis = data_analyser.analyse_wontfix_issues(df_wontfix)

        if configuration:
            df_wontfix['CVSS'] = pandas.to_numeric(df_wontfix['CVSS'])
            cwe_injection = data_analyser.analyse_by_applications(df_wontfix[df_wontfix['CVSS'] >= float(configuration['cvss_filter'])], configuration['applications'], injection_filter)
            cwe_iam = data_analyser.analyse_by_applications(df_wontfix[df_wontfix['CVSS'] >= float(configuration['cvss_filter'])], configuration['applications'], iam_filter)
            df_inject = pandas.DataFrame(cwe_injection, columns=["App Inject", "Count"])
            df_iam = pandas.DataFrame(cwe_iam, columns=["App IAM", "Count"])
            df_wontfix_applications = pandas.concat([df_inject, df_iam], axis=1)

    frames = []
    if len(df) > 0:
        frames.append(df)

    if len(df_applications) != 0:
        frames.append(df_applications)

    if len(df2) != 0 and len(df_wontfix_analysis) != 0:
        frames.append(pandas.concat([df2, df_separator, df_wontfix_analysis], axis=1))
    elif len(df2) != 0 and len(df_wontfix_analysis) == 0:
        frames.append(df2)
    elif len(df2) == 0 and len(df_wontfix_analysis) != 0:
        frames.append(df_wontfix_analysis)

    if len(df3) != 0:
        frames.append(df3)

    if len(df4) != 0:
        frames.append(df4)

    if len(df_wontfix_applications) != 0:
        frames.append(df_wontfix_applications)

    if len(frames) != 0:
        logger.log("debug", "generated dataframes - writing to excel now: " + excel)
        excel_adaptor.write_multiple_frames_to_one_sheet(frames, excel, ['data', 'data_app', 'analysis', 'dependencies', 'wontfix', 'wontfix_analysis'])
exit(0)
