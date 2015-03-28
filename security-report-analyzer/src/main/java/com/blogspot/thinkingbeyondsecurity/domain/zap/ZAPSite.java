package com.blogspot.thinkingbeyondsecurity.domain.zap;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 26.03.13
 * Time: 19:40
 */
@XmlRootElement
public class ZAPSite implements Serializable {
    private List<ZAPAlertItem> alerts = new ArrayList<ZAPAlertItem>();

    public ZAPSite(List<ZAPAlertItem> items) {
        this.alerts = items;
    }

    public ZAPSite() {

    }

    @XmlElement
    public List<ZAPAlertItem> getAlerts() {
        return alerts;
    }

    public void setAlerts(List<ZAPAlertItem> alerts) {
        this.alerts = alerts;
    }

    public void addAlert(ZAPAlertItem alert) {
        this.alerts.add(alert);
    }
}
