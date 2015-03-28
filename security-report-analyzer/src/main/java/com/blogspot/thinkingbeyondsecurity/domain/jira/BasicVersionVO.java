package com.blogspot.thinkingbeyondsecurity.domain.jira;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;

/**
 * (c) Liquid Code Security
 * Date: 05.03.13
 * Time: 20:33
 */
@XmlRootElement
public class BasicVersionVO implements Serializable {

    private Long projectId = 1L;
    private Long versionId = 1L;
    private String description = " -- ";
    private String versionName = " -- ";

    public BasicVersionVO() {

    }

    public BasicVersionVO(Long projectId, long versionId, String versionName, String description) {
        this.projectId = projectId;
        this.versionId = versionId;
        this.versionName = versionName;
        this.description = description;
    }

    @XmlElement
    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    @XmlElement
    public Long getProjectId() {
        return projectId;
    }

    public void setProjectId(Long projectId) {
        this.projectId = projectId;
    }

    @XmlElement
    public Long getVersionId() {
        return versionId;
    }

    public void setVersionId(Long versionId) {
        this.versionId = versionId;
    }

    @XmlElement
    public String getVersionName() {
        return versionName;
    }

    public void setVersionName(String versionName) {
        this.versionName = versionName;
    }
}
