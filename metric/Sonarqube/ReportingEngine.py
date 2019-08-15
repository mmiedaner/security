# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:29:04 2019

@author: xv01171
"""

from Util.DatabaseAdaptor import DatabaseAdaptor
from Util.ExcelAdaptor import ExcelAdaptor
from DataVisualizer import DataVisualizer
import pandas, json, datetime




def update_vuln_table(configuration):
    print ("Connecting to database" )
    da = DatabaseAdaptor()
    conn = da.getConnection(configuration['db_config'])
    
    query = "SELECT cve from vulnerability"
    results = da.executeQuery(conn, query, None)
    
    cves={}
    for result in results:
        cves[result[0]] = result[0]
       
    # --> extract vulnerabilities -> insert new ones
    cve_new={}
    for index,row in df.iterrows():
        if ("Filename:" in row['message']):
            mesg = row['message']
            
            cve = str(mesg.split("|")[1].split(":")[1]).strip()
            cve_new[cve]=cve
            
            temp = mesg.split("|")[3]
            if ("CWE" in  temp):
                temp2 = temp.split(":")[1]
                if (len(temp2) > 9):
                    cwe = str(temp2[1:8]).strip()
    
            cvss_score = str(mesg.split("|")[2].split(":")[1])
            
            if (len(mesg.split("|")) > 4):
                fours_element = str(mesg.split("|")[4]) 
                description = (fours_element[:199]) if len(fours_element) > 199 else fours_element
            else:
                description = None
            
            print (description)
            
            
            if cve not in cves:
                insert_query = "INSERT INTO vulnerability (`cve`, `cwe`, `cvss-score`, `description`) VALUES (%s, %s, %s, %s)" 
                da.insertIntoTable(conn, insert_query, (cve, cwe, cvss_score, description))
    
    da.cleanUp(conn)
    # remove old ones:

    conn2 = da.getConnection(configuration['db_config'])
    for c in cves:
        if c not in cve_new:
            query = "DELETE FROM vulnerability where cve= %s"
            da.executeQuery(conn2, query, (c,))
    
    da.cleanUp(conn2)
    
    
def update_days_open(resultSet, severities, run_date, sonar_name, configuration):
    insert_query= "INSERT into history_vulns_open (`count`, `severity`, `run_date`, `days_open`, `sonar_name`) values (%s, %s, %s, %s, %s);"
    
    da = DatabaseAdaptor()
    
    # Blocker = 0, Critical = 1, Major=2, Minor = 3, Info = 4.
    counter = 0
    while counter < 5:
        bin_1 = resultSet.iloc[:,counter]
        days = [125, 250, 375, 500, 625]
        day = 0

        for elm in bin_1:
            params = (str(elm), severities[counter], run_date,  str(days[day]), sonar_name)
            day += 1
            conn = da.getConnection(configuration['db_config'])
            da.insertIntoTable(conn, insert_query, params)

        counter += 1

    da.cleanUp(conn)
    
    

def update_history_vulns_project(resultSet, run_date, sonar_name, configuration):
    insert_query = "INSERT INTO history_vulns_project (`gh_user`, `run_date`, `severity`, `count`, `sonar_name`) VALUES (%s, %s, %s, %s, %s)"
    da = DatabaseAdaptor()
    
    conn = da.getConnection(configuration['db_config'])
    
    for index, row in resultSet.iterrows():
        params = (row['name'], str(run_date), row['severity'], str(row['count'][0]), sonar_name)
        da.insertIntoTable(conn, insert_query, params)
    
    da.cleanUp(conn)
    

def update_history_vulns_category(resultSet, run_date, sonar_name, configuration):
    insert_query = "INSERT INTO history_vulns_category (`gh_user`,`run_date`, `category`, `count`, `sonar_name`) VALUES (%s, %s, %s, %s, %s)"
    da = DatabaseAdaptor()
    
    conn = da.getConnection(configuration['db_config'])
    
    for index, row in resultSet.iterrows():
        params = (row['key'], str(run_date), row['category'], str(row['count']), sonar_name)
        da.insertIntoTable(conn, insert_query, params)
    
    da.cleanUp(conn)

def load_configuration():
    configuration = json.load(open("metric_config.json"))
    creds = json.load(open("creds.json"))
    configuration['db_config'] = creds['db_config']
    configuration['creds'] = creds['creds']
    return configuration


    
"""
## Anzahl Schwachstellen nach Severity und SE-Team: → Ableitung allgemeiner Schulungsbedarf

Anzahl der WEbinare pro Entwickler mit SecFocuss

"""


ea = ExcelAdaptor()
install_names = ["sonar", "sonarpuma", "sonarcloud"]
configuration = load_configuration()
datum1 = datetime.datetime.now().strftime("%Y-%m-%d")
dat = datum1.split("-")
datum = dat[0] + "-" + str(int(dat[1]) - 1)

for install_name in install_names:
    dv = DataVisualizer()

    path = "C:/Users/xv01171/Workspace/tools/metrics/"
    excel_file_name = path + datum + "_" + install_name + "_all.xls"
    
    df  = ea.read_sheet_from_excel(excel_file_name, "data")
    excel_input = ea.read_sheet_from_excel(excel_file_name, "data")
    df_excel_input = excel_input[['severity', 'creationDate', 'file', 'rule', 'project', 'message', 'status', 'tags']]
    
    keys = dv.get_column_values(df_excel_input, 'project', False)
    names = dv.get_column_values(df_excel_input, 'project', True)
    
    df_key = pandas.DataFrame(keys, columns=(['key']))
    df_projects = pandas.concat([df_excel_input, df_key], axis=1)
    
    severities = configuration['severities']
    color = configuration['color']
    owasp_categories = configuration['matrix']


    dv.do_one_pager(df_projects, configuration, names, "Sca_analysis_" + install_name + ".pdf")
    
    figure_file_name_3 = "Category_by_Project_" + install_name + ".jpg"
    resultSet = dv.plot_data_by_category_and_project(df_projects, names, owasp_categories, figure_file_name_3, True, 241)
    update_history_vulns_category(resultSet, datum1, install_name, configuration)

    figure_file_name_6 = "Severity_stacked_" + install_name + ".jpg"
    severities_simple = ["BLOCKER","CRITICAL", "MAJOR"]
    resultSet = dv.plot_data_by_severity_and_project(df_projects, names, color, severities_simple, figure_file_name_6, True, 242)

    figure_file_name_7 = "Mean_Age_with_Variance_"+ install_name + ".jpg"
    resultSet = dv.plot_data_by_average_age_and_sev(df_projects, severities, color, figure_file_name_7, True, 243)


    figure_file_name = "Severitiy_by_Days_Open_" + install_name + ".jpg"
    resultSet = dv.plot_data_by_severity_and_days_open(df_excel_input, figure_file_name, True)
    update_days_open(resultSet, severities, datum1, install_name, configuration)

    figure_file_name_2 = "Severity_by_Project_" + install_name + ".jpg"
    resultSet = dv.plot_data_by_severity_and_project(df_projects, names, color, severities, figure_file_name_2, True, 244)
    update_history_vulns_project(resultSet, datum1, install_name, configuration)
    
    figure_file_name_4 = "HeatMap_Anwendungen_" + install_name + ".jpg"
    resultSet = dv.plot_heatmap(df_excel_input, configuration['weighted_severities'], figure_file_name_4, True)
    
    figure_file_name_5 = "OWASP_Heat_Map_" + install_name + ".jpg"
    resultSet = dv.plot_owasp_heat_map(df_projects,  configuration['OWASP-Categories'], configuration['weighted_severities'], figure_file_name_5, True)

    figure_file_name_6 = "TOP_5_Findings_" + install_name + ".pdf"
    dv.get_top_5_findings(df_projects, severities, figure_file_name_6)