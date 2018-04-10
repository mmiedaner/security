import os
import xml.etree.ElementTree
import pandas


# source_dir = r'\\alm\reporting\trunk'
# root_prefix = '{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}'
source_dir = r'\\jenkins\reporting\trunk'
root_prefix = '{https://jeremylong.github.io/DependencyCheck/dependency-check.1.5.xsd}'

def read_files(name_of_file, report_data):
    root = xml.etree.ElementTree.parse(name_of_file).getroot()
    project_name = None
    report_date = None

    for pi in root.iter(root_prefix + 'projectInfo'):
        pn = pi.find(root_prefix + 'name')
        if pn is not None:
            project_name = pn.text

        rd = pi.find(root_prefix + 'reportDate')
        if rd is not None:
            report_date = rd.text

    item_count = len(report_data)

    for dependencies in root.findall(root_prefix + 'dependencies'):

        for dep in dependencies.iter(root_prefix + 'dependency'):

            file_name = None
            fn = dep.find(root_prefix + 'fileName')
            if fn is not None:
                file_name = fn.text

            for vuln in dep.iter(root_prefix + 'vulnerability'):
                vuln_name = None
                cvss_score = None
                cwe = None
                description = None

                name = vuln.find(root_prefix + 'name')
                if name is not None:
                    vuln_name = name.text

                score = vuln.find(root_prefix + 'cvssScore')
                if score is not None:
                    cvss_score = score.text

                fcwe = vuln.find(root_prefix + 'cwe')
                if fcwe is not None:
                    cwe = fcwe.text
                else:
                    cwe = None

                desc = vuln.find(root_prefix + 'description')
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
                # print 'reading: ' + os.path.join(root, file)
                read_files(os.path.join(root, file), report_data)
    return report_data


headerLine = ["projectName", "reportDate", "fileName", "vulnname", "cvssScore", "cwe", "description"]
df = pandas.DataFrame(analyse_xml_reports(source_dir), columns=headerLine)
df.to_excel("nexus_metrics.xls")

exit(0)
