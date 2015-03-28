package com.blogspot.thinkingbeyondsecurity.domain;

import com.atlassian.jira.issue.IssueInputParameters;
import org.w3c.dom.Document;

import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 17:12
 */
public interface ReportParser {
    List<IssueInputParameters> parse(Document xml);
}
