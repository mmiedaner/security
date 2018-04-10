import re

import numpy
import pandas

from ExcelAdaptor import ExcelAdaptor


class DataAnalyser:
    def group_vulns_in_libs_by_cvss(self, df_dependencies):
        """
        group vluns in libs by rounded cvss score and report all
        :param df_dependencies: dataframe to analyse
        :return: dataframe with analysis cvss-score | count
        """
        cvss_numeric = pandas.to_numeric(df_dependencies['CVSS'])
        bin0 = bin1 = bin2 = bin3 = bin4 = bin5 = bin6 = bin7 = bin8 = bin9 = bin10 = 0
        for row in cvss_numeric:
            value = round(row, 0)
            if value < 1:
                bin0 += 1
            elif value == 1:
                bin1 += 1
            elif value == 2:
                bin2 += 1
            elif value == 3:
                bin3 += 1
            elif value == 4:
                bin4 += 1
            elif value == 5:
                bin5 += 1
            elif value == 6:
                bin6 += 1
            elif value == 7:
                bin7 += 1
            elif value == 8:
                bin8 += 1
            elif value == 9:
                bin9 += 1
            elif value == 10:
                bin10 += 1
        return pandas.DataFrame(
            [["0", bin0], ["1", bin1], ["2", bin2], ["3", bin3], ["4", bin4], ["5", bin5], ["6", bin6], ["7", bin7],
             ["8", bin8], ["9", bin9], ["10", bin10]], columns=["CVSS-Score", "Count"])

    def group_by_columnanme(self, dataframe, column_name):
        """
        Count entries by columnname
        :param dataframe to analyse
        :return: analysis as columnname | Count
        """
        df = pandas.DataFrame({'Count': dataframe.groupby([column_name]).size()}).reset_index()
        return df

    def count_by_tag(self, dataframe, tags):
        """
        Count findings based on tag associated
        :param dataframe: dataframe to analyse
        :return: dataframe with analysis: owasp-tag | count
        """
        if tags and not dataframe['tags'].empty:
            data_to_return = []
            counter = 0
            for tag in tags:
                for datafield in dataframe['tags']:
                    if tag in datafield:
                        counter += 1
                data_to_return.append([tag, counter])
                counter = 0
        return pandas.DataFrame(data_to_return, columns=('TAG', 'TagCount'))

    def group_by_severity(self, dataframe):
        """
        Group Data by Severity and count findings.
        :param dataframe: to analyse
        :return: dataframe with analysis Severity | Count
        """
        blocker = dataframe[(dataframe['severity'] == 'BLOCKER')]['delta'].count()
        critical = dataframe[(dataframe['severity'] == 'CRITICAL')]['delta'].count()
        major = dataframe[(dataframe['severity'] == 'MAJOR')]['delta'].count()
        minor = dataframe[(dataframe['severity'] == 'MINOR')]['delta'].count()
        info = dataframe[(dataframe['severity'] == 'INFO')]['delta'].count()

        open_issues = dataframe['delta'].count()

        content = [["Blocker", blocker], ["Critical", critical],
                   ["Major", major], ["Minor", minor], ["Info", info], ["SUM Open", open_issues]]
        return pandas.DataFrame(content, columns=('Severity', 'Count'))

    def group_by_days_open(self, data):
        """
        Perform analysis of collected data
        :param data to analyse
        :return: dataframe with analysis (pivot table)
        """
        excel_adaptor = ExcelAdaptor()
        bins = numpy.arange(0, 750, 125)
        labels = [125, 250, 375, 500, 625]
        data['delta'] = pandas.to_numeric(data['delta'])
        return excel_adaptor.create_pivot_analysis(data, 'delta', 'labels', bins, labels, 'Tage Offen')

    def generate_dependency_checker_report(self, df):
        """
        Generate Report of OWASP DependencyChecker Data
        :param: dataframe to analyse
        :return: dataframe with report
        """
        lineitem_list = []
        for index, dat in df.iterrows():
            if 'message' in dat:
                msg = dat['message']
                str_msg = str(msg)

                if str_msg.startswith("Filename:"):
                    lineitem = []
                    lineitem.append(dat['project'])
                    attributes = str_msg.split("|")
                    i = 0

                    for attribute in attributes:
                        atr_str = str(attribute).lstrip()
                        value = ""
                        if atr_str.startswith("Reference:"):
                            value = atr_str.split(":")[1].lstrip().rstrip()
                        elif atr_str.startswith("CVSS Score:"):
                            value = atr_str.split(":")[1].lstrip().rstrip()
                        elif atr_str.startswith("Category"):
                            cwe_string = atr_str.split(":")[1].lstrip()
                            stop = cwe_string.index(" ")
                            lineitem.append(cwe_string[:stop])
                            value = atr_str  # to keep CWE-DESCRIPTION
                        elif i == 3 and not re.match("Category", str_msg):
                            lineitem.append(" ")
                            lineitem.append(str(attribute))
                        else:
                            value = str(attribute)
                        lineitem.append(value)
                        i += 1

                    lineitem_list.append(lineitem)

        df3 = pandas.DataFrame(lineitem_list,
                               columns=("project", "filename", "CVE", "CVSS", "CWE", "CWE-Description", "comment"))
        return df3

    def analyse_wontfix_issues(self, dataframe):
        """
        anaylse wontfix issues
        :param dataframe: dataframe to analyse
        :return: analysis result
        """
        data_grouped_project = self.group_by_columnanme(dataframe, 'project')
        data_grouped_cwe = self.group_by_columnanme(dataframe, 'CWE')
        data_grouped_cvss = self.group_vulns_in_libs_by_cvss(dataframe)
        data_total = pandas.DataFrame([dataframe['project'].count()], columns=['total'])
        return pandas.concat([data_grouped_project, data_grouped_cwe, data_grouped_cvss, data_total], axis=1)

    def analyse_by_applications(self, dataframe, applicationslist, cwe_filter):
        """
        Analyses dataframe based on project list and filters for CWE column
        :param dataframe: dataframe to analyse
        :param applicationslist: list to filter column project by
        :param cwe_filter: filter for cwe column
        :return: array app | count
        """
        result = []
        for app in applicationslist:
            counts = 0
            counts += dataframe[(dataframe['project'] == app) & dataframe['CWE'].isin(cwe_filter)]['project'].count()
            result.append([app, counts])

        return result

    def analyse(self, df_analysis, df_dependencies, tags):
        """
        Main Routine to perform all analysis with
        :param df_analysis: data for analysis
        :param df_dependencies: data for analysis of dependencies
        :param tags: owasp-tags or similiar to group results by
        :return: dataframe containing all results
        """
        data = df_analysis[df_analysis.delta.notnull()]

        df_age = self.group_by_days_open(data)

        df_sev = self.group_by_severity(data)

        # Add Count(Vulns) by Owasp Controls
        df_owasp = self.count_by_tag(df_analysis, tags)

        df_cvss = self.group_vulns_in_libs_by_cvss(df_dependencies)

        df_cwes = self.group_by_columnanme(df_dependencies, 'CWE')

        return pandas.concat([df_age, df_sev, df_owasp, df_cvss, df_cwes], axis=1)
