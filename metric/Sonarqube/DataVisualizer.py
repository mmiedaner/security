# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:55:27 2019

@author: xv01171
"""
import pandas
import numpy
import datetime
import matplotlib.pyplot as plt
from Util.DatabaseAdaptor import DatabaseAdaptor 

"""
DataVisualizer helps analysing / grouping and visualizing data for 
SDLC Metrics
"""
class DataVisualizer:

    def __init__(self):
        """ 
        Initial class with empty array for all figures plottet
        """
        self.figures = []
        self.figmant = plt.get_current_fig_manager
        self.data = {}
        # plt.disable_warnings(plt.figure.max_open_warning)
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def _get_data_for_owasp_heat_map(self, df_input, weighted_sevs, owasp_categories):
        """
        determine data for owasp heat map - count of vunls grouped by owasp category
        df_input: DataFrame to analyse
        weighted_sevs: Object to weight severities numerically (severity:weight)
        owasp_categories: owasp categories to group vulns by
        returns DataFrame (category | cat_count | sev_sum | key_count)
        where categorie is the owasp category, cat_count is the number of vulns within the categoriy, 
        sev_sum = is the sum of the weighted severities of the vulns within the owasp category and
        key_count is the number of porjects within the owasp category
        """
        df_data_cp = df_input[~df_input['rule'].str.contains("OWASP")][['severity', 'key', 'project', 'tags', 'status']]
        df_data_cp = self._add_numerical_severity(df_data_cp, weighted_sevs)
         
        df_data_cp = df_data_cp.dropna()
        cat_count = []
        sev_sum = []
        key_count = []
        
        data_matrix = []
        for cat in owasp_categories.keys():
            cat_count.append(df_data_cp[df_data_cp['tags'].str.contains(cat)]['status'].count())
            sev_sum.append(df_data_cp[df_data_cp['tags'].str.contains(cat)]['num_sev'].sum())
            key_count.append(df_data_cp[df_data_cp['tags'].str.contains(cat)]['key'].count())        
            data_matrix.append({"category":cat, "cat_count":cat_count, "sev_sum":sev_sum, "key_count":key_count})
        
        return pandas.DataFrame(data_matrix, columns={"category", "cat_count", "sev_sum", "key_count"})
    
    
    def _do_plot_owasp_heat_map(self, fig, owasp_data, owasp_categories, position):
        """
        plot a heat map of vulns by owasp category and count within category
        fig: figure to derive subplot from
        owasp_data: data to analyse
        owasp_categories: owasp categories to group data by
        position: position of table within a multi subplot plot
        """
        owasp_keys = owasp_data['category']
        cat_count = owasp_data['cat_count']
        sev_sum = owasp_data['sev_sum']
        key_count = owasp_data['key_count']
        
        sub2 = fig.add_subplot(position)
        sub2.yaxis.set_label("Anzahl Projekte in der Kategorie")
        sub2.xaxis.set_label("Anzahl Findings in der Kategorie")
        
        for i in range(0, len(cat_count)):
            sub2.scatter(cat_count[i], key_count[i], s=sev_sum[i], alpha=0.5)
            
        for j in range(0, len(owasp_keys)):
            sub2.axes.text(cat_count[0][j], key_count[0][j], owasp_keys[j])

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        
        textstr = ""
        for key in owasp_categories.keys():
            textstr += str(key) + " - " + str(owasp_categories[key]) + '\n'
        
        sub2.axes.text(1.1, 0.95, textstr, transform=sub2.axes.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)
        sub2.set_title("Offene Schwachstellen gruppiert nach OWASP Control Categorien")
    
  
    def _get_count_of_vulns_by_project(self, data, key_column_name, count_column_name ):
        """
        determine the number of vulns on a per project basis
        data: DataFrame to analyse
        key_column_name: column name within the DataFrame which contains project keys / names
        count_column_name: column to count occurences when data are grouped by key_column_name
        """
        names_unique= {}
        for key in data[key_column_name]:
            names_unique[key] = key
        
        data_matrix = []
        for name in names_unique:
            summe = data[data[key_column_name] == name][count_column_name].count()
            data_matrix.append({"name": name, "summe": summe})
            
            
        return pandas.DataFrame(data_matrix, columns={"name", "summe"})


    def _do_table_of_most_vulns(self, fig, df_data, position):
        """
        determine top most vulnerable projects and report as table
        fig: figure to derive table visualization from
        df_data: DataFrame to analyse
        position: position of table within a multi subplot plot
        """
        # Table        
        sub0 = fig.add_subplot(position)
        df_severity = self._get_count_of_vulns_by_project(df_data, "key", "status")
        table_data = df_severity.sort_values('summe', ascending=False).values
        
        # flip columns for pressi
        table_data[:,[0,1]] = table_data[:,[1,0]]
        
        sub0.axes.axis('tight')
        sub0.axes.axis('off')
        the_table = sub0.axes.table(cellText = table_data[0:9, :], colLabels=("Projekt", "Anzahl Schwachstellen"), loc='center')
        
        the_table.set_fontsize(14)
        the_table.scale(1.5,1.5)
        sub0.add_table(the_table)
        

    def _do_plot_sevs_by_project(self, df_data, fig, names, severities, color, position):
        """
        plots data as count of vulns grouped by severity for each project
        df_data: DataFrame to analyse
        fig: figure to derive subplot from
        names: project names to look for
        severities: severities to group vulns by
        color: colorscheme to plot data by
        position: position of table within a multi subplot plot
        """
        sub3 = fig.add_subplot(position)
        data_matrix = []   
        
        df_data.sort_values('count', ascending=False)
        
        for name in names:
            data = df_data[df_data['key'] == name]
            for severity in severities:
                if severity in data['severity'].values:
                    balken = data[data['severity'] == severity]['count'].values
                    if balken is not None and len(balken) > 0 and balken > 0:
                        sub3.barh(name, balken, color=color[severity], label=severity)
                        data_matrix.append({'name': name, 'count': balken, 'severity': severity})

        sub3.legend(labels=severities)
        sub3.xaxis.label.set_fontsize(12)
        sub3.yaxis.label.set_fontsize(14)
        sub3.set_autoscaley_on(True)
        sub3.set_title("Anzahl der Schwachstellen nach Projekt und Schwere")


    def _get_vulns_by_mean_age_and_variance(self, df_data, severities):
        """
        Determine the mean age and standard deviation of vulns in dataset
        df_data: DataFrame to analyse
        severities: severities to group vulns by.
        returns DataFrame: severity | age_mean | age_var
        """
        df_data_for_plot = self._add_days_open_column(df_data)
        datamatrix = []
        for severity in severities:
            age_mean = (df_data_for_plot[df_data_for_plot['severity'] == severity]['delta'].mean())
            age_var = (numpy.std(df_data_for_plot[df_data_for_plot['severity'] == severity]['delta']))
            datamatrix.append({'severity':severity, 'age_mean':age_mean, 'age_var':age_var})
        
        return pandas.DataFrame(datamatrix, columns={"severity", "age_mean", "age_var"})
        
    
    
    def _do_plot_mean_age_of_vulns(self, fig, data, color, position):
        """
        Plot number of vulns by mean age and standard deviation
        fig: fig to derive subplot from
        data: DataFrame to plot
        color: Object contaning color definitions for plots (from configuration)
        position: position in subplot / complete figure
        """
        sub4 = fig.add_subplot(position)
        sub4.axes.set_xlabel("Schwachstellen nach Gewichtung")
        sub4.axes.set_ylabel("Durschnittliches Alter der Schwachstellen")
        
        for index, row in data.iterrows():
            sub4.bar(row['severity'], row['age_mean'], yerr=row['age_var'], color=color[row['severity']], label=row['severity'])
            
        sub4.set_title("Offene Schwachstellen nach durchschnittlichem Alter und Schwere")
        sub4.legend()

    
    def _group_data_by_serverity(self, df_data, severities, names):
        """
        Group data by severities and project names. 
        :severities - list of severities to group data by
        :names - list of project names to group data by
        Returns a dataframe containing projectname, severity, count of issues found by projectname and severity
        """
        plot_data_matrix = []
        for project_name in names:
            for severity in severities:
                df_issues = df_data[(df_data['key'] == project_name) & (df_data['severity'] == severity)]['status'].count()
                data_row = {}
                data_row['key'] = project_name
                data_row['severity'] = severity
                data_row['count'] = int(df_issues)
                plot_data_matrix.append(data_row)
        return pandas.DataFrame(plot_data_matrix, columns={"key", "severity", "count"})
    
    
    def _add_days_open_column(self, df_input_data):
        """
        extends provided dataframe by a cloumn containing the count of days since the vuln was first detected
        :df_input_data - dataframe to analyse, needs to contain a column called creationDate
        returns dataframe extend by column called delta containing the count of days since the vuln was first detected
        """
        datum=[]
        for index,row in df_input_data.iterrows():
            date = datetime.datetime.strptime(row['creationDate'], "%Y-%m-%d")
            delta = datetime.datetime.now() - date
            datum.append(delta.days)

        df_datum = pandas.DataFrame(datum, columns=['delta'])
        return pandas.concat([df_input_data, df_datum], axis=1)


    def _add_numerical_severity(self, df_input_data, weighted_sevs):
        """
        extends provided dataframe by a column called num_sev containing the weight of the severity reported in the row
        : df_input_data - dataframe to extend
        : weighted_sevs - weights for each severity
        returns dataframe with column called num_sevs containing the weight of the severity reported in the row
        """
        num_sev = []
        for index, row in df_input_data.iterrows():
                num_sev.append(weighted_sevs[row['severity']])
        
        df_num_sev = pandas.DataFrame(num_sev, columns={"num_sev"})
        return pandas.concat([df_num_sev, df_input_data], axis=1)


    def _do_pie(self, fig, df_projects, labels, colors, position):
        """
        plots a pie chart of the vulns found to put the top 10 table into perspective
        df_projects: dataframe to analyze
        labels: labels to put on the plot
        colors: colors for the wedges
        """
        blocker = df_projects[df_projects['severity'] == 'BLOCKER']['file'] .count()
        critical = df_projects[df_projects['severity'] == 'CRITICAL']['file'].count()
        major = df_projects[df_projects['severity'] == 'MAJOR']['file'].count()
        minor = df_projects[df_projects['severity'] == 'MINOR']['file'].count()
        info = df_projects[df_projects['severity'] == 'INFO']['file'].count()
    
        summe = blocker + critical + major + minor + info
    
        data = []
        data.append((blocker/summe) * 100)
        data.append((critical/summe) * 100)
        data.append((major/summe)*100)
        data.append((minor/summe)*100)
        data.append((info/summe)*100)
        
        sub1 = fig.add_subplot(position)
        sub1.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        sub1.axes.axis('equal')


    def get_column_values(self, data, column_name, unique):
        """
        extract project names from data
        :data dataframe to extract project names from
        :unique if true return only unique names, if false return every project name found including dublicates
        """
        names_unique= {}
        names_nonu = []
            
        for index, row in data.iterrows():
            name = row['project'].split(":")[0]
            if unique:
                names_unique[name]=name
            else:
                names_nonu.append(name)
        
        if unique:
            return names_unique
        else:
            return names_nonu

            
    
    def plot_data_by_severity_and_project(self, data, names, color, severities, file_name, append, position):
        """
        plots data provided by severity and project name
        :data - dataframe containing vulns, severities and so on
        :names - names of the projects to look for in the dataframe
        :color - colors to paint the data in according to severity
        :severities - severities to group the data by
        :file_name - name of file to write the plot to
        returns the plotted data as dataframe and adds figure / plot to local array of figures
        """
        df_data_for_plot = self._group_data_by_serverity(data, severities, names)
        
        fig, ax = plt.subplots()
        plt.subplot(position)
        fig.set_figheight(25)
        fig.set_figwidth(25)
        data_matrix = []    
        for name in names:
            data = df_data_for_plot[df_data_for_plot['key'] == name]
            for severity in severities:
                if severity in data['severity'].values:
                    balken = data[data['severity'] == severity]['count'].values
                    if balken is not None and len(balken) > 0 and balken > 0:
                        ax.barh(name, balken, color=color[severity], label=severity)
                        data_matrix.append({'name': name, 'count': balken, 'severity': severity})
            
        plt.legend(labels=severities)
        plt.xlabel("Anzahl Schwachstellen offen")
        plt.title("Anzahl der Schwachstellen nach Projekt und Schwere")
        
        if not append:
            self.write_to_file(file_name)

        data = pandas.DataFrame(data_matrix, columns={"name", "count", "severity"})
        return data
  
    
    def plot_data_by_average_age_and_sev(self, df_data, severities, color, file_name, append, position):
        """
        plots data group by average age including standard deviation and severity
        :df_data - data to analyse
        :severities - serverities to group by
        :color - color to use for each severity
        :file_name - file name to save plot to
        determines automatically the days the vulns are open and calculates mean age including 
        standard deviation. Finally groups everything by severity and plots it as bar diagramm.
        Figure will be appended to local array
        """
        df_data_for_plot = self._add_days_open_column(df_data)
        
        fig, ax = plt.subplots()
        plt.subplot(position)
        plt.xlabel("Schwachstellen nach Gewichtung")
        plt.ylabel("Durschnittliches Alter der Schwachstellen")
        
        datamatrix = []
        for severity in severities:
            age_mean = (df_data_for_plot[df_data_for_plot['severity'] == severity]['delta'].mean())
            age_var = (numpy.std(df_data_for_plot[df_data_for_plot['severity'] == severity]['delta']))
            plt.bar(severity, age_mean, yerr=age_var, color=color[severity], label=severity)
            datamatrix.append({'severity':severity, 'age_mean':age_mean, 'age_var':age_var})
            
        plt.title("Offene Schwachstellen nach durchschnittlichem Alter und Schwere")
        plt.legend()
        data = pandas.DataFrame(datamatrix, columns={"severity", "age_mean", "age_var"})
        
        if not append:
            self.write_to_file(file_name)
        
        return data
        
    
    def plot_data_by_severity_and_days_open(self, df_data_for_plot_days_open, file_name, append):
        """
        plots data by severity and time / days open
        :df_data_for_plot_days_open - data frame to analys
        :file_name - name to save plot to
        Determines automatically how many days each vuln is open and groups it by the supplied severities.
        It appends plot to local figure array and returns the plotted dataframe for DB updates.
        """
        df_data_for_plot_days_open = self._add_days_open_column(df_data_for_plot_days_open)
        
        df_blocker = df_data_for_plot_days_open.loc[df_data_for_plot_days_open['severity'] == 'BLOCKER']
        df_critical = df_data_for_plot_days_open.loc[df_data_for_plot_days_open['severity'] == 'CRITICAL']
        df_major = df_data_for_plot_days_open.loc[df_data_for_plot_days_open['severity'] == 'MAJOR']
        df_minor = df_data_for_plot_days_open.loc[df_data_for_plot_days_open['severity'] == 'MINOR']
        df_info = df_data_for_plot_days_open.loc[df_data_for_plot_days_open['severity'] == 'INFO']
        
        df_plot_blocker = df_blocker.groupby(pandas.cut(df_blocker['delta'], bins=range(0, 750, 125), labels=range(125,750, 125))).count()
        df_plot_critical = df_critical.groupby(pandas.cut(df_critical['delta'], bins=range(0, 750, 125), labels=range(125,750, 125))).count()
        df_plot_major = df_major.groupby(pandas.cut(df_major['delta'], bins=range(0, 750, 125), labels=range(125,750, 125))).count()
        df_plot_minor = df_minor.groupby(pandas.cut(df_minor['delta'], bins=range(0, 750, 125), labels=range(125,750, 125))).count()
        df_plot_info = df_info.groupby(pandas.cut(df_info['delta'], bins=range(0, 750, 125), labels=range(125,750, 125))).count()
        
        fig, ax = plt.subplots()
        fig.set_figheight(15)
        fig.set_figwidth(15)
        
        scale= range(125, 750,125)
        plt.xlabel("Schwachstellen offen in Tagen")
        plt.ylabel("Anzahl Anwendungen")
        plt.plot(scale, df_plot_blocker['delta'], 'rs--', label="Blocker")
        plt.plot(scale, df_plot_critical['delta'], 'cs--', label="Critical")
        plt.plot(scale, df_plot_major['delta'], 'ys--', label="Major")
        plt.plot(scale, df_plot_minor['delta'], 'gs--', label="Minor") 
        plt.plot(scale, df_plot_info['delta'], 'bs--', label="Info")

        plt.title("Offene Schwachstellen nach Alter und Schwere")
        plt.legend()
        
        if not append:
            self.write_to_file(file_name)
            
        return pandas.concat([df_plot_blocker['delta'], df_plot_critical['delta'], df_plot_major['delta'], df_plot_minor['delta'], df_plot_info['delta']], axis=1)
    
    
    def plot_data_by_category_and_project(self, df_data_cp, names, owasp_categories, file_name, append, position):
        """
        plots vuln count group by owasp category and project names
        :df_data_cp - dataframe to analyse
        :names - project names
        :owasp_categories - owasp categories to group by
        :file_name - name of file to store figures in
        add plot to local array of figures and returns dataframe of plotted data
        """    
        df_data_cp = df_data_cp[~df_data_cp['rule'].str.contains("OWASP")][['severity', 'key', 'project', 'tags', 'status']]
    
        fig, ax = plt.subplots()
        plt.subplot(position)
        fig.set_figheight(25)
        fig.set_figwidth(25)
        
        data_matrix = []
        
        for project_name in names:
            
            tags = df_data_cp[df_data_cp['key'] == project_name]['tags'].values
            
            for category in owasp_categories:
                data_row = {}
                data_row['key'] = project_name
                data_row['category'] = category
    
                counter = 0
                for tag in tags:
                    if category in tag:
                        counter += 1
    
                data_row['count'] = counter
                if (counter > 0):
                    ax.barh(data_row['key'], data_row['count'], label=category) 
                    data_matrix.append({'key': data_row['key'], 'count': data_row['count'], 'category': category})
                
        plt.xlabel("Anzahl Schwachstellen offen")
        plt.title("Offene Schwachstellen nach Projekt und OWASP Control Category")
        plt.legend(labels=owasp_categories)
        
        if not append:
            self.write_to_file(file_name)

        data = pandas.DataFrame(data_matrix, columns=['key', 'count', 'category'])
        return data
    
    
    def plot_dependencies_by_severity(self, severities, config, color, file_name, append):
        """
        plots number of severities which are excluded from the owasp dependency checker form database.
        That means that the db must be up to date first
        :severities - severities to group the data by
        :color - color scheme for severity groups
        :file_name - name of file to write plot to
        returns nothing, appends plot to local array of figures
        """
        
        config['raise_on_warnings'] = True 
        
        da = DatabaseAdaptor()
        conn = da.getConnection(config)
        query = "select gh_user, project, severity from finding where cve in (select cve from vulnerability)"
        record = da.executeQuery(conn, query, None)
        
        df_dependencies = pandas.DataFrame(record, columns=["gh_user", "project", "severity"])
        keys = {}
        
        for gh_user in df_dependencies['gh_user']:
            keys[gh_user] = gh_user
    
    
        fig, ax = plt.subplots()
        
        for gh_user in keys:
            for severity in severities:
                count = df_dependencies[(df_dependencies['gh_user'] == gh_user) & (df_dependencies['severity'] == severity)]['project'].count()
                if (count > 0):
                    ax.barh(gh_user, count, label=severity, color=color[severity]) 
        
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.xlabel("Anzahl Schwachstellen offen")
        plt.title("Offene Schwachstellen in ausgeklammerten Bibliotheken nach Schwere")
        plt.legend()
        if not append:
            self.write_to_file(file_name)
        
    
    def plot_heatmap(self, df_input, weighted_severities, file_name, append):
        """
        plots data by age and weighted severity. Size of the bubble represents the number of vulns found.
        :df_input - dataframe to analyse
        :weighted_severities - weights for the severities to analyse
        :file_name - name of file to write plot to
        returns nothing, appends plot to local array of figures
        """
        df_input = self._add_days_open_column(df_input)
        df_input = self._add_numerical_severity(df_input, weighted_severities)
        
        dat_project = []
        dat_sev = []
        dat_age = []
        dat_count = []
        keys = self.get_project_names(df_input, True)
        for key in keys:
            
            num_sev = 0
            for sev in weighted_severities.keys():
                num_sev += df_input[(df_input['project'] == key) & (df_input['severity'] == str(sev))]['num_sev'].sum()
            
            dat_project.append(key)
            dat_sev.append(num_sev)
            dat_age.append(df_input[df_input['project'] == key]['delta'].max())
            dat_count.append(df_input[df_input['project'] == key]['delta'].count())
        
        fig, ax = plt.subplots()
      
        plt.ylabel("Summe gewichteter Schwere")
        plt.xlabel("Anzahl Tage offen")
        plt.scatter(dat_age, dat_sev, s=dat_count)
        plt.title("Offene Schwachstellen nach Alter und gewichteter Schwere")
        if not append:
            self.write_to_file(file_name)
 

    def plot_owasp_heat_map(self, df_input, owasp_categories, weighted_sevs, file_name, append):
        """
        plots data grouped by owasp category and projects. Size of the bubble is the weighted severity
        :df_input - dataframe to analyse
        :owasp_categories - categories to group data by
        :weighted_severities - weights for the severities to group data by
        :file_name - name of file to write data to
        returns nothing, appends plot to local array of figures
        """
        df_data_cp = df_input[~df_input['rule'].str.contains("OWASP")][['severity', 'key', 'project', 'tags', 'status']]
        df_data_cp = self._add_numerical_severity(df_data_cp, weighted_sevs)
         
        df_data_cp = df_data_cp.dropna()
        
        cat_count = []
        sev_sum = []
        key_count = []
        
        owasp_keys = list(owasp_categories.keys())
        
        for cat in owasp_categories.keys():
            cat_count.append(df_data_cp[df_data_cp['tags'].str.contains(cat)]['status'].count())
            sev_sum.append(df_data_cp[df_data_cp['tags'].str.contains(cat)]['num_sev'].sum())
            key_count.append(df_data_cp[df_data_cp['tags'].str.contains(cat)]['key'].count())
             
        fig, ax = plt.subplots()
        fig.set_figheight(18)
        fig.set_figwidth(18)
        plt.ylabel("Anzahl Projekte in der Kategorie")
        plt.xlabel("Anzahl Findings in der Kategorie")
        
        plt.scatter(cat_count, key_count, s=sev_sum, alpha=0.5)
        
        for i in range(0, len(key_count)):
            ax.annotate(owasp_keys[i], xy=(cat_count[i], key_count[i]))

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        
        textstr = ""
        for key in owasp_categories.keys():
            textstr += str(key) + " - " + str(owasp_categories[key]) + '\n'
        
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
        plt.title("Offene Schwachstellen gruppiert nach OWASP Control Categorien")
        
        if not append:
            self.write_to_file(file_name)


    def do_one_pager(self, df_input, configuration, names, file_name):
        """
        create One Pager after specification by mirko saam
        df_input: DataFrame to work on
        configuration: configuration object based on metric_config.json
        names: Array of project names
        file_name: Name of file to write plots to
        """
        owasp_categories = configuration['OWASP-Categories']
        weighted_sevs = configuration['weighted_severities']
        color = configuration['color']
        severities = configuration['severities']
        
        #Table - sub0
        fig = plt.figure(figsize=(45, 20))
        plt.subplots_adjust(right=0.8)
        self._do_table_of_most_vulns(fig, df_input, 161)
        
        
        #PIE Chart - sub1
        self._do_pie(fig, df_input, severities, ['r', 'c', 'y', 'g', 'b'], 162)
        
        
        #HeatMap - sub2
        df_owasp = self._get_data_for_owasp_heat_map(df_input, weighted_sevs, owasp_categories)
        self._do_plot_owasp_heat_map(fig, df_owasp, owasp_categories, 163)
        

        # Severity by Projekt -> Top 5 - sub3
        df_data_for_plot = self._group_data_by_serverity(df_input, severities, names)
        # self._do_plot_sevs_by_project(df_data_for_plot, fig)
        self._do_plot_sevs_by_project(df_data_for_plot, fig, names, ["BLOCKER","CRITICAL", "MAJOR"], color, 165)
        
        
        # Mean age and variance by severity - sub 4
        df_data_mean_age = self._get_vulns_by_mean_age_and_variance(df_input, severities)
        self._do_plot_mean_age_of_vulns(fig, df_data_mean_age, color, 166)
        
        plt.tight_layout()
        plt.savefig(file_name)
        plt.close()


    def get_top_5_findings(self, df_projects, severities, file_name):
        """
        get the top 5 security findings per sonar installation
        df_projects: data_frame to analyze
        severities: severities to group / filter the data by
        file_name: name of file to write the result to
        returns nothing - just writes the file
        """
        
        df_data = df_projects[['severity', 'file', 'project']].sort_values('severity', ascending=True)
        
        fig = plt.figure(figsize=(20, 20))
        
        sub0 = fig.add_subplot(111)
        table_data = []
        for index, row in df_data.head(6).iterrows():
            table_data.append([row['file'], row['severity'], row['project']])
        
        the_table = sub0.axes.table(cellText = table_data, colLabels=("Datei", "Schwere", "Projekt"), loc='center')
        the_table.set_fontsize(24)
        sub0.add_table(the_table)
        sub0.axes.axis('tight')
        sub0.axes.axis('off')
        
        plt.tight_layout()
        plt.savefig(file_name)
        plt.close()


    def write_to_file(self, file_name):
        """
        writes all figures from local array into an pdf file
        :file_name - name of file to write to
        returns nothing.
        """
        
        plt.savefig(file_name)
        plt.close()