package com.blogspot.thinkingbeyondsecurity.domain.zap;

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
 * Date: 30.03.13
 * Time: 17:09
 */
public class ZapReportParser implements ReportParser {

    private final static String SITE_ITEM = "site";
    private final static String ALERTS_LIST = "alerts";
    private final static String ALERTS_ITEM = "alertitem";

    @Override
    public List<IssueInputParameters> parse(Document xml) {
        NodeList nodeList = xml.getDocumentElement().getChildNodes();
        List<ZAPAlertItem> zapAlerts = new ArrayList<ZAPAlertItem>();
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node firstLevel = nodeList.item(i);
            if (firstLevel != null && firstLevel.getNodeName().equals(SITE_ITEM) && firstLevel.hasChildNodes()) {
                NodeList alertLists = firstLevel.getChildNodes();
                for (int j = 0; j < alertLists.getLength(); j++) {
                    Node alertList = alertLists.item(j);
                    if (alertList != null && alertList.getNodeName().equals(ALERTS_LIST) && alertList.hasChildNodes()) {
                        NodeList alertItems = alertLists.item(j).getChildNodes();
                        for (int k = 0; k < alertItems.getLength(); k++) {
                            Node xmlAlertItem = alertItems.item(k);
                            if (xmlAlertItem != null && xmlAlertItem.getNodeName().equals(ALERTS_ITEM) && xmlAlertItem.hasChildNodes()) {
                                ZAPAlertItem alertItem = new ZAPAlertItem();
                                NodeList content = xmlAlertItem.getChildNodes();
                                for (int l = 0; l < content.getLength(); l++) {
                                    Node contentItem = content.item(l);
                                    if (contentItem.getNodeName().equals("pluginid")) {
                                        alertItem.setPluginId(getTextContextAsLong(contentItem));
                                    }
                                    if (contentItem.getNodeName().equals("alert")) {
                                        alertItem.setAlert(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("riskcode")) {
                                        alertItem.setRiskcode(getTextContextAsLong(contentItem));
                                    }
                                    if (contentItem.getNodeName().equals("reliability")) {
                                        alertItem.setReliability(getTextContextAsLong(contentItem));
                                    }
                                    if (contentItem.getNodeName().equals("riskdesc")) {
                                        alertItem.setRiscdesc(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("desc")) {
                                        alertItem.setDesc(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("uri")) {
                                        alertItem.setUri(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("param")) {
                                        alertItem.setParam(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("attack")) {
                                        alertItem.setAttack(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("otherinfo")) {
                                        alertItem.setOtherinfo(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("solution")) {
                                        alertItem.setSolution(contentItem.getTextContent());
                                    }
                                    if (contentItem.getNodeName().equals("reference")) {
                                        alertItem.setReference(contentItem.getTextContent());
                                    }
                                }
                                zapAlerts.add(alertItem);
                            }
                        }
                    }
                }
            }
        }
        return createJiraIssueFromZapAlertItems(zapAlerts);
    }

    private String getPriorityForAlertItem(ZAPAlertItem item) {
        if (item.getReliability() == 2 & item.getRiskcode() == 2) {
            // return JiraConstants.PRIORITY_HIGH;
            return "1";
        } else if (item.getReliability() == 2 & item.getRiskcode() == 1) {
            // return JiraConstants.PRIORITY_MEDIUM;
            return "2";
        } else if (item.getReliability() == 2 & item.getRiskcode() == 0) {
            // return JiraConstants.PRIORITY_LOW;
            return "3";
        } else if (item.getReliability() == 1 & (item.getRiskcode() == 2 || item.getRiskcode() == 1)) {
            // return JiraConstants.PRIORITY_MEDIUM;
            return "2";
        } else {
            // return JiraConstants.PRIORITY_LOW;
            return "3";
        }
    }

    private List<IssueInputParameters> createJiraIssueFromZapAlertItems(List<ZAPAlertItem> alertItems) {
        List<IssueInputParameters> issuesToCreate = new ArrayList<IssueInputParameters>();
        for (ZAPAlertItem item : alertItems) {
            IssueInputParameters issueInputParameters = new IssueInputParametersImpl();

            String summary = item.getAlert() + " : " + item.getUri();
            // jira summary needs to be less then 255 Chars
            if (summary.length() > 254) {
                issueInputParameters.setSummary(summary.substring(0, 254));
            } else {
                issueInputParameters.setSummary(summary);
            }

            String description = summary + "\n" + item.getDesc() + " \n " + item.getSolution() + " \n " + item.getReference();
            issueInputParameters.setDescription(description);


            issueInputParameters.setPriorityId(getPriorityForAlertItem(item));

            issuesToCreate.add(issueInputParameters);
        }
        return issuesToCreate;
    }

    private long getTextContextAsLong(Node item) {
        long result = Long.MIN_VALUE;
        try {
            result = Long.valueOf(item.getTextContent());
        } catch (NumberFormatException nfe) {
            //TODO how to handle that case?
        }
        return result;
    }

}
