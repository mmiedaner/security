package com.blogspot.thinkingbeyondsecurity;

import com.atlassian.jira.config.ConstantsManager;
import com.atlassian.jira.issue.issuetype.IssueType;
import com.atlassian.jira.issue.resolution.Resolution;
import com.atlassian.sal.api.ApplicationProperties;
import com.blogspot.thinkingbeyondsecurity.domain.jira.BasicIssueTypeVO;
import com.blogspot.thinkingbeyondsecurity.domain.jira.BasicResolutionVO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.CacheControl;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;


@Path("/extension")
@Consumes({MediaType.APPLICATION_JSON})
@Produces({MediaType.APPLICATION_JSON})
public class SecurityReportAnalyzerImpl implements SecurityReportAnalyzer {
    private final ApplicationProperties applicationProperties;
    private final ConstantsManager constantsManager;
    private static final Logger log = LoggerFactory.getLogger(SecurityReportAnalyzerImpl.class);
    private CacheControl NO_CACHE = new CacheControl();

    public SecurityReportAnalyzerImpl(ApplicationProperties applicationProperties, ConstantsManager constantsManager) {
        this.applicationProperties = applicationProperties;
        this.constantsManager = constantsManager;
    }

    @GET
    @Path("/resolution")
    public Response getResolutions() {

        Collection<Resolution> resolutionList = constantsManager.getResolutionObjects();
        List<BasicResolutionVO> basicResolutionVOList = new ArrayList<BasicResolutionVO>();
        for (Resolution resolution : resolutionList) {
            BasicResolutionVO basicResolution = new BasicResolutionVO();
            basicResolution.setId(resolution.getId());
            basicResolution.setName(resolution.getName());
            basicResolutionVOList.add(basicResolution);
        }

        return Response.ok(basicResolutionVOList).cacheControl(NO_CACHE).build();
    }

    @GET
    @Path("/issueType")
    public Response getIssueTypes() {

        Collection<IssueType> issueTypeList = constantsManager.getAllIssueTypeObjects();
        List<BasicIssueTypeVO> basicIssueTypeVOList = new ArrayList<BasicIssueTypeVO>();
        for (IssueType issueType : issueTypeList) {
            BasicIssueTypeVO basicIssueType = new BasicIssueTypeVO();
            basicIssueType.setId(issueType.getId());
            basicIssueType.setName(issueType.getName());
            basicIssueTypeVOList.add(basicIssueType);
        }

        return Response.ok(basicIssueTypeVOList).cacheControl(NO_CACHE).build();
    }
}