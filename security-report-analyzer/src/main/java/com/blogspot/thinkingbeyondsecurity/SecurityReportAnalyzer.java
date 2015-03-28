package com.blogspot.thinkingbeyondsecurity;

import javax.ws.rs.core.Response;

public interface SecurityReportAnalyzer {

    public Response getResolutions();

    public Response getIssueTypes();

}