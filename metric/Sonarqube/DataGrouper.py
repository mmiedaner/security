import argparse

import pandas
from pandas.core.frame import DataFrame

file_name = None
regex_list = None
group_list = None
output_name = None
sheet_name = None
column_name = None


def parser_arguments():
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarquebe based on repositories of rules.')
    parser.add_argument('--input', metavar='input', help='name of input file')
    parser.add_argument('--output', metavar='output', help='name of output file')
    parser.add_argument('--append', metavar='append', help='append onto outputfile [yes | no]')
    parser.add_argument('--groups', metavar='regex', help='name for group to name for result', nargs='+')
    parser.add_argument('--sheetname', metavar='sheet_static', help='name of the sheet_static that should be analyzed')
    parser.add_argument('--regex', metavar='regex', help='regex to match against values of a certain column', nargs='+')
    parser.add_argument('--columnname', metavar='columnname', help='regex to match against columnnames')

    args = parser.parse_args()

    global file_name
    file_name = args.input

    global regex_list
    regex_list = args.regex

    global group_list
    group_list = args.groups

    global output_name
    output_name = args.output

    global sheet_name
    sheet_name = args.sheetname

    global column_name
    column_name = args.columnname


def get_findings_count_by(group, regex, sev, excel_input):
    count = 0
    for i in excel_input.index:
        field_name = excel_input[column_name][i]
        group_name = excel_input['component'][i]
        severity = excel_input['severity'][i]
        status = excel_input['status'][i]

        if group in group_name and sev == severity and status == "OPEN":
            if regex == "*" or regex == "all":
                count += 1
            elif regex in field_name:
                count += 1
    return count;


def build_dataframe(group_list, regex_list, excel_input):
    df_out = pandas.DataFrame(columns=('Name', 'Severity', 'Count'))

    j = 0

    for group in group_list:
        blocker = 0
        critical = 0
        major = 0
        minor = 0
        info = 0

        for regex in regex_list:
            blocker += get_findings_count_by(group, regex, "BLOCKER", excel_input)
            critical += get_findings_count_by(group, regex, "CRITICAL", excel_input)
            major += get_findings_count_by(group, regex, "MAJOR", excel_input)
            minor += get_findings_count_by(group, regex, "MINOR", excel_input)
            info += get_findings_count_by(group, regex, "INFO", excel_input)

        content = [[group, "Blocker", blocker], [group, "Critical", critical],
                   [group, "Major", major], [group, "Minor", minor], [group, "Info", info]]

        print ("GROUP= " + group + " blocker= " + str(blocker) + " critical= " + str(critical) + " major= " + str(
            major) + " minor= " + str(minor) + " info= " + str(info))

        if j == 0:
            df_out = DataFrame(content, columns=('Name', 'Severity', 'Count'), index=[j, j + 1, j + 2, j + 3, j + 4])
        else:
            step = j * 4
            df_out = df_out.append(DataFrame(content, columns=('Name', 'Severity', 'Count'),
                                             index=[j + step, j + step + 1, j + step + 2, j + step + 3, j + step + 4]))
        j += 1
    return df_out


##
## main routine
##
parser_arguments()

excel_input = pandas.ExcelFile(file_name).parse(sheet_name)

df_final = build_dataframe(group_list, regex_list, excel_input)
df_final.to_excel(output_name, sheet_name='sheet1', index=True)
