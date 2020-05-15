import base64
import json
import pandas
import glob
import re
import csv
import argparse

def parse_file(file):
    b64_string = ""
    with open(file) as in_file:
        i = 0
        for line in in_file:
            i += 1
            if i > 512 and "</script>" in line:
                break
            if i == 512:
                line_string = line.split('("')[1]
                string = line_string.replace("+", '')
                string_ = string.replace('"','')
                b64_string += string_
            if i > 512:
                line_string = line.replace('"', '')
                line_string_ = line_string.replace("+", '')
                b64_string += line_string_

    decoded_string = ""
    try:
        decoded_string = str(base64.b64decode(b64_string[:-5]), 'utf-8', errors="replace")
    except:
        print("An error occured  - Could not decode file: " +file)
        return None

    re.sub(r'"httpRequestUnescaped":\s"(.*?)",', '', decoded_string)
    re.sub(r'"httpRequest":\s"(.*?)",','', decoded_string)
    re.sub(r'"httpRequestUnescaped":[\s\S]*?(?="isBase64Encoded")', '', decoded_string)

    data = ""
    try:
        data = json.loads(str(decoded_string), strict=False)
    except:
        print("An error has occured - Could not parse file: " + file)
        return None

    data_array = []
    for item in data['items']:
        data_array.append(
            [item['method'], item['url'], item['responseCode'], item['rawRequest']['actualSize'], item['id'], item['requestDatetime']])
    return data_array


def read_directory(path):
    data = []
    file_count = error_count = 0
    for filename in glob.glob(path):
        file_count += 1
        data_from_file = parse_file(filename)
        if data_from_file is None:
            error_count += 1
        else:
            data += data_from_file

    df = pandas.DataFrame(data, columns=["Method", "Url", "ResponseCode", "Size", "Id", "Timestamp"])

    print ("-------------")
    print ("Files parsed: ", file_count)
    print ("Files in error: ", error_count)

    return df

def shorten_sync_urls(url, merge_attributes):
    for attribute in merge_attributes:
        if attribute in url:
            return url.rsplit('/', 1)[0]

    return url

def analyse_data(data, merge, merge_attributes):
    result = {}
    for index, row in data.iterrows():
        if merge:
            url_string = shorten_sync_urls(str(row['Url']), merge_attributes)

        if url_string in result:
            count = result[url_string] + 1
            result[url_string] = count
        else:
            result[url_string] = 1
    return result

def adjust_data_types():
    #Timestamps
    data['Timestamp'] = pandas.to_datetime(data['Timestamp'])


def analyse_request_by_date(csv_file, data):
    df = data.groupby(['Url', 'Timestamp']).describe()
    df.to_csv(csv_file + "_complete_report.csv")


def create_file_with_average_request_size(file_name, data, result):
    dat = []
    for key in result.keys():
        mean = data[data['Url'].str.contains(key)]['Size'].mean()
        dat.append([key, result[key], round(mean, 2)])

    df = pandas.DataFrame(dat, columns=['Url', 'Count', 'AvSize'])
    df.to_csv(file_name + "_avSize.csv", index=False)


def write_csv_file(csv_file, csv_columns, dict_data):
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)

            writer.writeheader()
            for key in dict_data.keys():
                writer.writerow({csv_columns[0]: key, csv_columns[1]: dict_data[key]})

    except IOError:
        print("I/O error")

def parse_args():
    parser = argparse.ArgumentParser(description='Extract data from event exports from F5 WAF/ASM for metrical analysis.', prog="WAFAlyzer", usage="--sDir <directory of exports> --output file_name.csv")
    parser.add_argument('--sDir', metavar='sDir', help='director to read the F5 exports from', required="True")
    parser.add_argument('--output', metavar='output', help='name of output file', required="True")
    parser.add_argument('--merge', metavar='merge', help='merge url containing this string and split by last /', nargs="*")
    parser.add_argument('--analysis', metavar='analysis', help='type of analysis that should be performed: Simple, AddAverage, All', nargs="*", default="All")
    global args
    args = parser.parse_args()

if __name__ == '__main__':
    parse_args()
    data = read_directory(args.sDir)
    merge = False
    merge_attributes = ""
    if args.merge and len(args.merge) > 0:
        merge = True
        merge_attributes = args.merge

    result = analyse_data(data, merge, merge_attributes)
    if "Simple" in args.analysis:
        write_csv_file(args.output, ["URL", "COUNT"], result)
    if "AdAverage" in args.analysis:
        create_file_with_average_request_size(args.output, data, result)
    if "All" in args.analysis:
        analyse_request_by_date(args.output, data)
    print("Finally done")