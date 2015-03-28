package com.blogspot.thinkingbeyondsecurity.util;

import webwork.multipart.MultiPartRequestWrapper;

import java.util.Enumeration;

/**
 * (c) Liquid Code Security
 * Date: 18.04.13
 * Time: 10:29
 */
public class ReportConfiguration {
    private String fileType;
    private String projectId;
    private String versionId;
    private String falsePosResolution;

    private String preferredIssueType;

    public ReportConfiguration(MultiPartRequestWrapper wrapper) {
        Enumeration e0 = wrapper.getParameterNames();
        while (e0.hasMoreElements()) {
            String paramName = e0.nextElement().toString();
            if (paramName.equals("fileType")) {
                this.fileType = wrapper.getParameterValues(paramName)[0];
            } else if (paramName.equals("projectId")) {
                this.projectId = wrapper.getParameterValues(paramName)[0];
            } else if (paramName.equals("versionId")) {
                this.versionId = wrapper.getParameterValues(paramName)[0];
            } else if (paramName.equals("falsePosResolution")) {
                this.falsePosResolution = wrapper.getParameterValues(paramName)[0];
            } else if (paramName.equals("preferredIssueType")) {
                this.preferredIssueType = wrapper.getParameterValues(paramName)[0];
            }
        }
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public String getVersionId() {
        return versionId;
    }

    public void setVersionId(String versionId) {
        this.versionId = versionId;
    }

    public String getFalsePosResolution() {
        return falsePosResolution;
    }

    public void setFalsePosResolution(String falsePosResolution) {
        this.falsePosResolution = falsePosResolution;
    }

    public String getPreferredIssueType() {
        return preferredIssueType;
    }

    public void setPreferredIssueType(String preferredIssueType) {
        this.preferredIssueType = preferredIssueType;
    }
}