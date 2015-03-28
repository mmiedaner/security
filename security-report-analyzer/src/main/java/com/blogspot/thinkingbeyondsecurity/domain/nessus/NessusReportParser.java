package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import com.atlassian.jira.issue.IssueInputParameters;
import com.atlassian.jira.issue.IssueInputParametersImpl;
import com.blogspot.thinkingbeyondsecurity.domain.ReportParser;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import java.util.ArrayList;
import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 01.04.13
 * Time: 19:39
 */
public class NessusReportParser implements ReportParser {

    private static final String NESSUS_REPORT = "Report";
    private static final String NESSUS_REPORT_HOST = "ReportHost";
    private static final String NESSUS_REPORT_ITEM = "ReportItem";
    private static final String NESSUS_REPORT_HOST_NAME = "name";
    private static final String NESSUS_REPORT_PLUGINNAME = "pluginName";
    private static final String NESSUS_REPORT_SEVERITY = "severity";
    private static final String NESSUS_REPORT_SOLUTION = "solution";
    private static final String NESSUS_REPORT_DESCRIPTION = "description";
    private static final String NESSUS_REPORT_PLUGIN_OUTPUT = "plugin_output";


    private String hostURI;

    @Override
    public List<IssueInputParameters> parse(Document xml) {
        NodeList nodeList = xml.getDocumentElement().getChildNodes();
        NessusReport nessusReport = new NessusReport();

        for (int i = 0; i < nodeList.getLength(); i++) {
            Node report = nodeList.item(i);

            if (report != null && report.getNodeName().equals(NESSUS_REPORT) && report.hasChildNodes()) {
                NodeList reportHosts = report.getChildNodes();

                for (int j = 0; j < reportHosts.getLength(); j++) {
                    Node reportHost = reportHosts.item(j);

                    if (reportHost != null && reportHost.getNodeName().equals(NESSUS_REPORT_HOST) && reportHost.hasChildNodes()) {
                        NessusReportHost nessusReportHost = new NessusReportHost();

                        nessusReportHost.setName(reportHost.getAttributes().getNamedItem(NESSUS_REPORT_HOST_NAME).getTextContent());

                        NodeList reportItems = reportHost.getChildNodes();
                        for (int k = 0; k < reportItems.getLength(); k++) {

                            Node reportItem = reportItems.item(k);
                            if (reportItem != null && reportItem.getNodeName().equals(NESSUS_REPORT_ITEM)) {

                                NessusReportItem nessusReportItem = new NessusReportItem();
                                nessusReportItem.setPluginName(reportItem.getAttributes().getNamedItem(NESSUS_REPORT_PLUGINNAME).getTextContent());

                                int severity = convertToIntSafely(reportItem.getAttributes().getNamedItem(NESSUS_REPORT_SEVERITY).getTextContent());
                                nessusReportItem.setSeverity(severity);

                                if (reportItem.hasChildNodes()) {

                                    NodeList reportItemChildren = reportItem.getChildNodes();

                                    for (int l = 0; l < reportItemChildren.getLength(); l++) {
                                        Node child = reportItemChildren.item(l);
                                        if (child.getNodeName().equals(NESSUS_REPORT_SOLUTION)) {
                                            nessusReportItem.setSolution(child.getTextContent());
                                        }
                                        if (child.getNodeName().equals(NESSUS_REPORT_DESCRIPTION)) {
                                            nessusReportItem.setDescription(child.getTextContent());
                                        }
                                        if (child.getNodeName().equals(NESSUS_REPORT_PLUGIN_OUTPUT)) {
                                            nessusReportItem.setPluginOutput(child.getTextContent());
                                        }
                                    }

                                }
                                nessusReportHost.addNessusReportItem(nessusReportItem);
                            }
                        }
                        nessusReport.addNessusReportHost(nessusReportHost);
                    }
                }
            }

        }
        return createJiraIssueFromNessusReport(nessusReport);
    }

    private List<IssueInputParameters> createJiraIssueFromNessusReport(NessusReport report) {
        List<IssueInputParameters> issuesToCreate = new ArrayList<IssueInputParameters>();
        for (NessusReportHost host : report.getNessusReportHosts()) {
            for (NessusReportItem item : host.getNessusReportItems()) {
                IssueInputParameters inputParameters = new IssueInputParametersImpl();
                inputParameters.setPriorityId(mapSeverityToPriority(item.getSeverity()));

                String summaryString = item.getPluginName() + " : " + host.getName();
                // jira summary needs to be less then 255 Chars
                if (summaryString.length() > 254) {
                    inputParameters.setSummary(summaryString.substring(0, 254));
                } else {
                    inputParameters.setSummary(summaryString);
                }

                String descriptionString = summaryString + "\n" + "Synopsis: \n" + item.getSynopsis() + "\n Attack: " + item.getPluginOutput() + "\n Solution: \n" + item.getSolution();
                inputParameters.setDescription(descriptionString);

                issuesToCreate.add(inputParameters);
            }
        }
        return issuesToCreate;
    }

    private String mapSeverityToPriority(int severity) {
        if (severity >= 3) {
            // return JiraConstants.PRIORITY_HIGH;
            return "1";
        } else if (severity == 2) {
            // return JiraConstants.PRIORITY_MEDIUM;
            return "2";
        } else {
            // return JiraConstants.PRIORITY_LOW;
            return "3";
        }
    }

    private int convertToIntSafely(String value) {
        int returnValue = Integer.MIN_VALUE;
        try {
            returnValue = Integer.valueOf(value);
        } catch (NumberFormatException nfe) {
            // TODO what to do now?
        }
        return returnValue;
    }
}
