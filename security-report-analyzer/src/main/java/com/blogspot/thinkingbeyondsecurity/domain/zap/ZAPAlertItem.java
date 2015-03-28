package com.blogspot.thinkingbeyondsecurity.domain.zap;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;

/**
 * (c) Liquid Code Security
 * Date: 26.03.13
 * Time: 19:41
 */
@XmlRootElement
public class ZAPAlertItem implements Serializable {
    private long pluginId;
    private String alert;
    private long riskcode;
    private long reliability;
    private String riscdesc;
    private String desc;
    private String uri;
    private String param;
    private String attack;
    private String otherinfo;
    private String solution;
    private String reference;

    public ZAPAlertItem() {

    }

    @XmlElement
    public long getPluginId() {
        return pluginId;
    }

    public void setPluginId(long pluginId) {
        this.pluginId = pluginId;
    }

    @XmlElement
    public String getAlert() {
        return alert;
    }

    public void setAlert(String alert) {
        this.alert = alert;
    }

    @XmlElement
    public long getRiskcode() {
        return riskcode;
    }

    public void setRiskcode(long riskcode) {
        this.riskcode = riskcode;
    }

    @XmlElement
    public long getReliability() {
        return reliability;
    }

    public void setReliability(long reliability) {
        this.reliability = reliability;
    }

    @XmlElement
    public String getRiscdesc() {
        return riscdesc;
    }

    public void setRiscdesc(String riscdesc) {
        this.riscdesc = riscdesc;
    }

    @XmlElement
    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    @XmlElement
    public String getUri() {
        return uri;
    }

    public void setUri(String uri) {
        this.uri = uri;
    }

    @XmlElement
    public String getParam() {
        return param;
    }

    public void setParam(String param) {
        this.param = param;
    }

    @XmlElement
    public String getAttack() {
        return attack;
    }

    public void setAttack(String attack) {
        this.attack = attack;
    }

    @XmlElement
    public String getOtherinfo() {
        return otherinfo;
    }

    public void setOtherinfo(String otherinfo) {
        this.otherinfo = otherinfo;
    }

    @XmlElement
    public String getSolution() {
        return solution;
    }

    public void setSolution(String solution) {
        this.solution = solution;
    }

    @XmlElement
    public String getReference() {
        return reference;
    }

    public void setReference(String reference) {
        this.reference = reference;
    }
}
