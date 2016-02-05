import argparse
import pandas
from pandas.core.frame import DataFrame

file_name = None
regex_list = None
group_list = None
output_name = None
sheet_name = None

def parser_arguments():
    parser = argparse.ArgumentParser(
        description='Collect issue statistics from sonarquebe based on repositories of rules.')
    parser.add_argument('--input', metavar='input', help='name of input file')
    parser.add_argument('--output', metavar='output', help='name of output file')
    parser.add_argument('--append', metavar='append', help='append onto outputfile [yes | no]')
    parser.add_argument('--cregex', metavar='regex', help='regex to match against componentnames', nargs='+')
    parser.add_argument('--groups', metavar='regex', help='name for group to name for result', nargs='+')
    parser.add_argument('--sheetname', metarv='sheet', help='name of the sheet that should be analyzed')
    args = parser.parse_args()

    global file_name
    file_name = args.input

    global regex_list
    regex_list = args.cregex

    global group_list
    group_list = args.groups

    global output_name
    output_name = args.output
    
    global sheet_name
    sheet_anem = args.sheetname

def get_metrics_from_excel(excel_input, regex_list, group_list):
    df_out = pandas.DataFrame(columns=('Name', 'Severity', 'Count'))
    j = 0
    for regex in regex_list:
        blocker = 0
        critical = 0
        major = 0
        minor = 0
        info = 0
        for i in excel_input.index:
            component_name = excel_input['componentName'][i]
            if regex in component_name:
                severity = excel_input['severity'][i]
                if severity == "BLOCKER":
                    blocker += 1
                if severity == "CRITICAL":
                    critical += 1
                if severity == "MAJOR":
                    major += 1
                if severity == "MINOR":
                    minor += 1
                if severity == "INFO":
                    info += 1

        content = [[group_list[j], "Blocker", blocker], [group_list[j], "Critical", critical],
                   [group_list[j], "Major", major], [group_list[j], "Minor", minor], [group_list[j], "Info", info]]
        if j == 0:
            df_out = DataFrame(content, columns=('Name', 'Severity', 'Count'), index=[j, j + 1, j + 2, j + 3, j + 4])
        else:
            df_intermediate = df_out
            step = j * 4
            df_out = df_out.append(DataFrame(content, columns=('Name', 'Severity', 'Count'),
                                 index=[j + step, j + step + 1, j + step + 2, j + step + 3, j + step + 4]))
        j += 1
    
    return df_out

## Main Method
parser_arguments()
excel_input = pandas.ExcelFile(file_name)._parse_xlsx(sheet_name)
df_final = get_metrics_from_excel(excel_input, regex_list, group_list)
df_final.to_excel(output_name, sheet_name='sheet1', index=True)
