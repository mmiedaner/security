import datetime
import os

path_to_sonar_script = ".\SonarMetricsExtractor.py"
path_to_simple_sonar_script = ".\SonarClient.py"
path_to_grouper_script = ".\DataGrouper.py"
path_to_python = 'python.exe'
sonar_base_url = "https://sonar.ruv.de:8443"
install_names = ["/sonar", "/sonarpuma", "/sonarcloud"]

datum1 = datetime.datetime.now().strftime("%Y-%m-%d")
dat = datum1.split("-")
datum = dat[0] + "-" + str(int(dat[1]) - 1)


i = 0
while i < len(install_names):
        
        print ("collection cwe and findbugssec data from " + str(install_names[i]))
        
        file_name6 = datum + "_" 
        if len(install_names[i]) >  0:
            file_name6 += str(install_names[i])[1:]
        file_name6 += "_all"

        command6 = path_to_python + " " + path_to_sonar_script + " --lang java --baseurl " + sonar_base_url + " --tags owasp-a1 owasp-a2 owasp-a3 owasp-a4 owasp-a5 owasp-a6 owasp-a7 owasp-a8 owasp-a9 owasp-a10 --date_separator T --excel " + file_name6 + ".xls" + " --analyze True --config metric_config.json --creds creds.json --install_name " + str(install_names[i])
        os.system(command6)
        print (command6)
        i += 1

file_name2 = datum + "_sonar_all"


print ("grouping cwe and findbugsec data by injection attacks")
file_name3 = datum + "_inject.xls"
command3 = path_to_python + " " + path_to_grouper_script + " --input " + file_name2 + ".xls --output " + file_name3 + " --append yes --sheetname data --columnname rule --groups Zentrale zenDS MeineRuV Geraete Abschlussstrecke-Kfz Admin Aib Antibot Bav Evb Kredit Ktv Baustein Condor Makler Rv24 Tarifrechner Vrrente WTM Gdv 1Portal --regex DMI HRS SQL COMMAND_INJECTION FILE_UPLOAD PATH_TRAVERSAL STRUTS_FORM UNVALIDATED_REDIRECT WEAK_FILENAME XPATH XSS XXE"
os.system(command3)
print (command3 + "\n")

print ("grouping cwe and findbugsec data by krypto attacks" )
file_name4 = datum + "_krypto.xls"
command4 = path_to_python + " " + path_to_grouper_script + " --input " + file_name2 + ".xls  --output " + file_name4 + " --append yes --sheetname data --columnname rule --groups Zentrale zenDS MeineRuV Geraete Abschlussstrecke-Kfz Admin Aib Antibot Bav Evb Kredit Ktv Baustein Condor Makler Rv24 Tarifrechner Vrrente WTM Gdv 1Portal --regex BAD_HEXA CIPHER PREDICTABLE STATIC_IV UNENCRYPTED WEAK_MESSAGE"
os.system(command4)
print (command4 + "\n")

print ("grouping all findings by portal name")
file_name5 = datum + "_portal.xls"
command5 = path_to_python + " " + path_to_grouper_script + " --input " + file_name2 + ".xls --output " + file_name5 + " --append yes --sheetname data --columnname rule --groups MeineRuV Abschlussstrecke-Kfz zenDS Tarifrechner Geraete WTM Condor Makler 1Portal Rv24 Bav Evb Kredit Vrrente Ktv Gdv Admin Aib Antibot Zentrale Baustein --regex all"
os.system(command5)
print (command5 + "\n")

print ("Done collecting data from SonarQube.")
print ("Done!!")