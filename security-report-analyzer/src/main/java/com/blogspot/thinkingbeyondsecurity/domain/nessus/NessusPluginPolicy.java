package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 16:42
 */

@XmlRootElement
public class NessusPluginPolicy {

    private String pluginName;
    private long pluginId;
    private String fullName;
    private String preferenceName;
    private String preferenceType;
    private String preferenceValues;
    private String selectedValue;

    @XmlElement
    public String getPluginName() {
        return pluginName;
    }

    public void setPluginName(String pluginName) {
        this.pluginName = pluginName;
    }

    @XmlElement
    public long getPluginId() {
        return pluginId;
    }

    public void setPluginId(long pluginId) {
        this.pluginId = pluginId;
    }

    @XmlElement
    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    @XmlElement
    public String getPreferenceName() {
        return preferenceName;
    }

    public void setPreferenceName(String preferenceName) {
        this.preferenceName = preferenceName;
    }

    @XmlElement
    public String getPreferenceType() {
        return preferenceType;
    }

    public void setPreferenceType(String preferenceType) {
        this.preferenceType = preferenceType;
    }

    @XmlElement
    public String getPreferenceValues() {
        return preferenceValues;
    }

    public void setPreferenceValues(String preferenceValues) {
        this.preferenceValues = preferenceValues;
    }

    @XmlElement
    public String getSelectedValue() {
        return selectedValue;
    }

    public void setSelectedValue(String selectedValue) {
        this.selectedValue = selectedValue;
    }
}
