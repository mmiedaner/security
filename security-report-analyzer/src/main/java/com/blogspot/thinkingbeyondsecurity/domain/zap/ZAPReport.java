package com.blogspot.thinkingbeyondsecurity.domain.zap;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;
import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 26.03.13
 * Time: 17:45
 */

@XmlRootElement
public class ZAPReport implements Serializable {

    private List<ZAPSite> zapSite;

    public ZAPReport() {

    }

    public ZAPReport(List<ZAPSite> sites) {
        this.zapSite = sites;
    }


    @XmlElement
    public List<ZAPSite> getZapSite() {
        return zapSite;
    }

    public void setZapSite(List<ZAPSite> zapSite) {
        this.zapSite = zapSite;
    }
}
