package com.blogspot.thinkingbeyondsecurity.util;

import com.atlassian.crowd.embedded.api.User;
import com.atlassian.jira.bc.issue.IssueService;
import com.atlassian.jira.bc.issue.search.SearchService;
import com.atlassian.jira.issue.Issue;
import com.atlassian.jira.issue.IssueInputParameters;
import com.atlassian.jira.issue.search.SearchException;
import com.atlassian.jira.jql.builder.JqlClauseBuilder;
import com.atlassian.jira.jql.builder.JqlQueryBuilder;
import com.atlassian.jira.web.bean.PagerFilter;
import com.google.common.collect.Maps;

import java.util.List;
import java.util.Map;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 18:37
 */
public class JiraInteractionHelper {

    public Map<String, Object> createIssue(IssueInputParameters issueInputParameters, IssueService issueService, User user) {
        Map<String, Object> context = Maps.newHashMap();
        IssueService.CreateValidationResult result = issueService.validateCreate(user, issueInputParameters);

        if (result.getErrorCollection().hasAnyErrors()) {
            // If the validation fails, render the list of issues with the error in a flash message

            context.put("errors", result.getErrorCollection().getErrors());
        } else {
            // If the validation passes, redirect the user to the main issue list page
            issueService.create(user, result);
            context.put("success", "success");
        }
        return context;
    }

    public List<Issue> getIssues(SearchService searchService, String projectId, User user) {

        // The search interface requires JQL clause... so let's build one
        JqlClauseBuilder jqlClauseBuilder = JqlQueryBuilder.newClauseBuilder();

        com.atlassian.query.Query query = jqlClauseBuilder.project(projectId).buildQuery();
        // A page filter is used to provide pagination. Let's use an unlimited filter to
        // to bypass pagination.
        PagerFilter pagerFilter = PagerFilter.getUnlimitedFilter();

        com.atlassian.jira.issue.search.SearchResults searchResults = null;
        try {
            searchResults = searchService.search(user, query, pagerFilter);
        } catch (SearchException e) {
            e.printStackTrace();
        }
        return searchResults.getIssues();
    }
}
