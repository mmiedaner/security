package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 16:34
 */
@XmlRootElement
public class NessusReportItem {

    private int port;
    private String svcName;
    private String protocol;
    private int severity;
    private int pluginId;
    private String pluginName;
    private String pluginFamily;
    private String solution;
    private String riskFactor;
    private String description;
    private String synopsis;
    private String pluginType;
    private String pluginModificationDate;
    private String pluginOutput;
    private String pluginVersion;

    @XmlElement
    public String getSolution() {
        return solution;
    }

    public void setSolution(String solution) {
        this.solution = solution;
    }

    @XmlElement
    public String getRiskFactor() {
        return riskFactor;
    }

    public void setRiskFactor(String riskFactor) {
        this.riskFactor = riskFactor;
    }

    @XmlElement
    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    @XmlElement
    public String getSynopsis() {
        return synopsis;
    }

    public void setSynopsis(String synopsis) {
        this.synopsis = synopsis;
    }

    @XmlElement
    public String getPluginType() {
        return pluginType;
    }

    public void setPluginType(String pluginType) {
        this.pluginType = pluginType;
    }

    @XmlElement
    public String getPluginModificationDate() {
        return pluginModificationDate;
    }

    public void setPluginModificationDate(String pluginModificationDate) {
        this.pluginModificationDate = pluginModificationDate;
    }

    @XmlElement
    public String getPluginOutput() {
        return pluginOutput;
    }

    public void setPluginOutput(String pluginOutput) {
        this.pluginOutput = pluginOutput;
    }

    @XmlElement
    public String getPluginVersion() {
        return pluginVersion;
    }

    public void setPluginVersion(String pluginVersion) {
        this.pluginVersion = pluginVersion;
    }

    @XmlElement
    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    @XmlElement
    public String getSvcName() {
        return svcName;
    }

    public void setSvcName(String svcName) {
        this.svcName = svcName;
    }

    @XmlElement
    public String getProtocol() {
        return protocol;
    }

    public void setProtocol(String protocol) {
        this.protocol = protocol;
    }

    @XmlElement
    public int getSeverity() {
        return severity;
    }

    public void setSeverity(int severity) {
        this.severity = severity;
    }

    @XmlElement
    public int getPluginId() {
        return pluginId;
    }

    public void setPluginId(int pluginId) {
        this.pluginId = pluginId;
    }

    @XmlElement
    public String getPluginName() {
        return pluginName;
    }

    public void setPluginName(String pluginName) {
        this.pluginName = pluginName;
    }

    @XmlElement
    public String getPluginFamily() {
        return pluginFamily;
    }

    public void setPluginFamily(String pluginFamily) {
        this.pluginFamily = pluginFamily;
    }
}
