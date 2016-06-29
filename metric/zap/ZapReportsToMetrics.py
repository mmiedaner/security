import os
import argparse
from lxml import etree
from pandas.core.frame import DataFrame

args = None
source_dir = "<your source dir>"
metrics = None


def extract_file_content(file_name):
    high_count = 0
    medium_count = 0
    low_count = 0
    info_count = 0

    parser = etree.HTMLParser()
    tree = etree.parse(file_name, parser)
    root_element = tree.getroot()

    # root_element[0] = head
    # root_element[1] = body
    for child in list(root_element[1]):
        if child.tag == "table":
            #table[0] == Summary
            #tr0 = headline
            #tr1,5 - td1 - font - a -> Severity
            #tr1,5 - td2 - font -> Count
            max_tr = len(list(child))
            i = 1
            while i < max_tr:
                tr = list(child)[i]
                a_tag = tr[0][0][0]
                i += 1
                if a_tag.tag == "a":
                    severity = a_tag.text
                    value = tr[1][0].text
                    if severity == "High":
                        high_count = value
                    elif severity == "Medium":
                        medium_count = value
                    elif severity == "Low":
                        low_count = value
                    elif severity == "Informational":
                        info_count = value

            group = file_name.split("_")[1].split(".")[0]
            content = [[group, "High", high_count], [group, "Medium", medium_count], [group, "Low", low_count],
                       [group, "Info", info_count]]
            return content


def parse_args():
    parser = argparse.ArgumentParser(description='Extract data from ZAP Reports for metrical analysis.')
    parser.add_argument('--sDir', metavar='sDir', help='director to read the ZAP reports from')
    parser.add_argument('--format', metavar='format', help='file format of the reports to read')
    parser.add_argument('--output', metavar='output', help='name of output file')
    global args
    args = parser.parse_args()


def handle_reports(sourcedir):
    for root, dirs, files in os.walk(sourcedir):
        j = 0
        for file in files:
            #TODO handle xml files
            if file.endswith("." + str(args.format)):
                content = extract_file_content(os.path.join(root, file))
                if j == 0:
                    df_out = DataFrame(content, columns=('Name', 'Severity', 'Count'), index=[j, j + 1, j + 2, j + 3])
                else:
                    step = j * 3
                    df_out = df_out.append(DataFrame(content, columns=('Name', 'Severity', 'Count'),
                                                     index=[j + step, j + step + 1, j + step + 2, j + step + 3]))
            j += 1
    return df_out

## main
parse_args()
data_frame = handle_reports(source_dir)
data_frame.to_excel(args.output, sheet_name='sheet1', index=True)
