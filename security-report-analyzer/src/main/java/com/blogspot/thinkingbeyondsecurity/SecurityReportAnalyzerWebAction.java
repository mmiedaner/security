package com.blogspot.thinkingbeyondsecurity;

import com.atlassian.crowd.embedded.api.User;
import com.atlassian.jira.bc.issue.IssueService;
import com.atlassian.jira.bc.issue.search.SearchService;
import com.atlassian.jira.bc.project.ProjectService;
import com.atlassian.jira.issue.Issue;
import com.atlassian.jira.issue.IssueInputParameters;
import com.atlassian.jira.issue.search.SearchException;
import com.atlassian.jira.jql.builder.JqlClauseBuilder;
import com.atlassian.jira.jql.builder.JqlQueryBuilder;
import com.atlassian.jira.web.action.JiraWebActionSupport;
import com.atlassian.jira.web.bean.PagerFilter;
import com.atlassian.seraph.auth.DefaultAuthenticator;
import com.blogspot.thinkingbeyondsecurity.domain.nessus.NessusReportParser;
import com.blogspot.thinkingbeyondsecurity.domain.zap.ZapReportParser;
import com.blogspot.thinkingbeyondsecurity.util.ReportConfiguration;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;
import webwork.action.ActionContext;
import webwork.action.ServletActionContext;
import webwork.multipart.MultiPartRequestWrapper;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 21.03.13
 * Time: 10:45
 */
public class SecurityReportAnalyzerWebAction extends JiraWebActionSupport {

    private static final String fileName = "file";
    private IssueService issueService;
    private ProjectService projectService;
    private SearchService searchService;
    private com.atlassian.jira.user.util.UserManager jiraUserManager;
    private static final Logger log = LoggerFactory.getLogger(SecurityReportAnalyzerWebAction.class);


    public SecurityReportAnalyzerWebAction(IssueService issueService, ProjectService projectService, SearchService searchService,
                                           com.atlassian.jira.user.util.UserManager jiraUserManager) {
        this.issueService = issueService;
        this.projectService = projectService;
        this.searchService = searchService;
        this.jiraUserManager = jiraUserManager;
    }

    protected void doValidation() {

    }

    protected String doExecute() {
        MultiPartRequestWrapper wrapper = (MultiPartRequestWrapper) ServletActionContext.getRequest();
        ReportConfiguration reportConfiguration = new ReportConfiguration(wrapper);
        Document xml = null;
        try {
            xml = getFileAsDocument(wrapper);
        } catch (Exception ex) {
            log.error("Could not parse file from upload");
            return "error";
        }
        if (!validateReportConfiguration(reportConfiguration)) {
            log.error("Could not validate configuration posted");
            return "error";
        }

        List<IssueInputParameters> issuesToCreate = new ArrayList<IssueInputParameters>();

        if (reportConfiguration.getFileType().equals("zap")) {
            ZapReportParser zapReportParser = new ZapReportParser();
            issuesToCreate = zapReportParser.parse(xml);
            log.debug("Will create " + issuesToCreate.size() + " issues");
        } else if (reportConfiguration.getFileType().equals("nessus")) {
            NessusReportParser nessusReportParser = new NessusReportParser();
            issuesToCreate = nessusReportParser.parse(xml);
            log.debug("Will create " + issuesToCreate.size() + " issues");
        } else {
            log.error("Unknown ReportType");
            return "error";
        }

        User user = (User) ActionContext.getSession().get(DefaultAuthenticator.LOGGED_IN_KEY);
        // get existing issues:
        List<Issue> oldIssues = getOldIssues(user, reportConfiguration);
        List<IssueInputParameters> issuesToFinallyCreate = new ArrayList<IssueInputParameters>();
        for (IssueInputParameters issue : issuesToCreate) {
            boolean found = false;
            for (Issue oldIssue : oldIssues) {
                if (oldIssue.getSummary().equals(issue.getSummary())) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                issuesToFinallyCreate.add(issue);
            }
        }

        for (IssueInputParameters issueToCreate : issuesToFinallyCreate) {
            ProjectService.GetProjectResult projectByKey = projectService.getProjectByKey(user, reportConfiguration.getProjectId());

            Long[] affectedVersion = new Long[1];
            affectedVersion[0] = Long.valueOf(reportConfiguration.getVersionId());
            issueToCreate.setAffectedVersionIds(affectedVersion);
            issueToCreate.setReporterId(user.getName());
            issueToCreate.setProjectId(projectByKey.getProject().getId());
            issueToCreate.setAssigneeId(projectByKey.getProject().getLeadUser().getName());
            issueToCreate.setIssueTypeId(reportConfiguration.getPreferredIssueType());

            IssueService.CreateValidationResult result = issueService.validateCreate(user, (IssueInputParameters) issueToCreate);

            if (result.getErrorCollection().hasAnyErrors()) {
                log.error("An error has occurred: {}", result.getErrorCollection());
            } else {
                issueService.create(user, result);
            }
        }
        return "success";
    }

    private boolean validateReportConfiguration(ReportConfiguration configuration) {
        if (configuration.getFalsePosResolution() == null) {
            return false;
        } else if (configuration.getFileType() == null) {
            log.error("No fileType transmitted");
            return false;
        } else if (configuration.getPreferredIssueType() == null) {
            log.error("No preferred issue type transmitted");
            return false;
        } else if (configuration.getProjectId() == null) {
            log.error("No ProjectId transmitted");
            return false;
        } else if (configuration.getVersionId() == null) {
            log.error("No VersionId transmitted");
            return false;
        }
        return true;
    }

    private List<Issue> getOldIssues(User user, ReportConfiguration reportConfiguration) {
        JqlClauseBuilder jqlClauseBuilder = JqlQueryBuilder.newClauseBuilder();
        if (StringUtils.isNotBlank(reportConfiguration.getFalsePosResolution())) {
            jqlClauseBuilder.resolution().eq(reportConfiguration.getFalsePosResolution()).and().project(reportConfiguration.getProjectId());
        } else {
            jqlClauseBuilder.project(reportConfiguration.getProjectId());
        }

        com.atlassian.query.Query query = jqlClauseBuilder.buildQuery();
        // A page filter is used to provide pagination. Let's use an unlimited filter to
        // to bypass pagination.
        PagerFilter pagerFilter = PagerFilter.getUnlimitedFilter();
        com.atlassian.jira.issue.search.SearchResults searchResults = null;
        try {
            // Perform search results
            searchResults = searchService.search(user, query, pagerFilter);
        } catch (SearchException e) {
            log.error("An exception occurred while searching issue {}", e);
        }
        return searchResults.getIssues();
    }

    private Document getFileAsDocument(MultiPartRequestWrapper wrapper) throws IOException, SAXException, ParserConfigurationException {
        Document xml = null;
        File f = wrapper.getFile(fileName);
        byte[] data = IOUtils.toByteArray(new FileInputStream(f));
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setValidating(false);
        factory.setNamespaceAware(false);
        DocumentBuilder builder = factory.newDocumentBuilder();
        xml = builder.parse(new ByteArrayInputStream(data));
        return xml;
    }

}
