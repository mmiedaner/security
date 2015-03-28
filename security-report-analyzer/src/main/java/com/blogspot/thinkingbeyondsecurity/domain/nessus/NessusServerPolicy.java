package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 16:40
 */
@XmlRootElement
public class NessusServerPolicy {

    private String name;
    private String value;

    @XmlElement
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @XmlElement
    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
