package com.blogspot.thinkingbeyondsecurity.domain.jira;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;

/**
 * (c) Liquid Code Security
 * Date: 22.04.13
 * Time: 16:47
 */
@XmlRootElement
public class BasicIssueTypeVO implements Serializable {

    private String id;
    private String name;

    public BasicIssueTypeVO() {

    }

    public BasicIssueTypeVO(String id, String name) {
        this.id = id;
        this.name = name;
    }

    @XmlElement
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    @XmlElement
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
