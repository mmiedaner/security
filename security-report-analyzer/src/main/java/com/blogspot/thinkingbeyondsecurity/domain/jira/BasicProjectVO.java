package com.blogspot.thinkingbeyondsecurity.domain.jira;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;

/**
 * (c) Liquid Code Security
 * Date: 05.03.13
 * Time: 20:52
 */
@XmlRootElement
public class BasicProjectVO implements Serializable {


    private Long projectId = 1L;
    private String name = " -- ";

    public BasicProjectVO() {

    }

    public BasicProjectVO(Long projectId, String name) {
        this.projectId = projectId;
        this.name = name;
    }

    @XmlElement
    public Long getProjectId() {
        return projectId;
    }

    public void setProjectId(Long projectId) {
        this.projectId = projectId;
    }

    @XmlElement
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
