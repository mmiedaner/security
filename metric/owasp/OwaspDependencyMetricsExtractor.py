import os
import xml.etree.ElementTree

import pandas


source_dir = '' # add your source directory for xml/html export from owasp dependency checker here.


def read_files(name_of_file, report_data):
    root = xml.etree.ElementTree.parse(name_of_file).getroot()
    project_name = None
    report_date = None

    for pi in root.iter('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}projectInfo'):
        pn = pi.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}name')
        if pn is not None:
            project_name = pn.text

        rd = pi.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}reportDate')
        if rd is not None:
            report_date = rd.text

    item_count = len(report_data)

    for dependencies in root.findall('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}dependencies'):

        for dep in dependencies.iter('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}dependency'):

            file_name = None
            fn = dep.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}fileName')
            if fn is not None:
                file_name = fn.text

            for vuln in dep.iter('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}vulnerability'):
                vuln_name = None
                cvss_score = None
                cwe = None
                description = None

                name = vuln.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}name')
                if name is not None:
                    vuln_name = name.text

                score = vuln.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}cvssScore')
                if score is not None:
                    cvss_score = score.text

                fcwe = vuln.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}cwe')
                if fcwe is not None:
                    cwe = fcwe.text
                else:
                    cwe = None

                desc = vuln.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}description')
                if desc is not None:
                    description = desc.text

                if vuln_name is not None:
                    line_item = [project_name, report_date, file_name, vuln_name, cvss_score.replace(".", ","), cwe,
                                 description]
                    report_data.append(line_item)

    if item_count == len(report_data):
        print "Found 0 vulns found (adding empty line) in file: " + name_of_file
        line_item = [project_name, report_date, "None", "None", -1, "None", "None"]
        report_data.append(line_item)
    else:
        print "Found " + str(len(report_data) + item_count) + " vulns in file: " + name_of_file


def analyse_xml_reports(sourcedir):
    report_data = []
    for root, dirs, files in os.walk(sourcedir):
        for file in files:
            if file.endswith(".xml"):
                read_files(os.path.join(root, file), report_data)
    return report_data


headerLine = ["projectName", "reportDate", "fileName", "vulnname", "cvssScore", "cwe", "description"]
df = pandas.DataFrame(analyse_xml_reports(source_dir), columns=headerLine)
df.to_excel("nexus_metrics.xls")
