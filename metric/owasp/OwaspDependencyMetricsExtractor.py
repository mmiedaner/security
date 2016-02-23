import os
import xml.etree.ElementTree

source_dir = '' #TODO place your source dir here


def write_line_to_file(file, line):
    file.write(line)


def read_files(nameOfFile, file):
    root = xml.etree.ElementTree.parse(nameOfFile).getroot()
    project_name = None
    report_date = None

    for pi in root.iter('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}projectInfo'):
        pn = pi.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}name')
        if pn is not None:
            project_name = pn.text

        rd = pi.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}reportDate')
        if rd is not None:
            report_date = rd.text

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
                    cwe = "NONE"

                desc = vuln.find('{https://www.owasp.org/index.php/OWASP_Dependency_Check#1.2}description')
                if desc is not None:
                    description = desc.text

                if vuln_name is not None:
                    line_item = project_name + "\t" + report_date + "\t" + file_name + "\t" + vuln_name + "\t" \
                                + cvss_score.replace(".", ",") + "\t" + cwe + "\t" + description + "\n"
                    write_line_to_file(file, line_item)


def analyse_xml_reports(sourcedir, f):
    for root, dirs, files in os.walk(sourcedir):
        for file in files:
            if file.endswith(".xml"):
                print 'reading: ' + os.path.join(root, file)
                read_files(os.path.join(root, file), f)


f = file('nexus_metrics.csv', 'w')
headerLine = 'projectName\treportDate\tfileName\tvulnname\tcvssScore\tcwe\tdescription\n'
write_line_to_file(f, headerLine)
analyse_xml_reports(source_dir, f)
f.close()
