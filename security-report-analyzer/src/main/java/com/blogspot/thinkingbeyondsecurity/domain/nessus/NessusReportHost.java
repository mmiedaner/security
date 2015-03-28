package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.util.ArrayList;
import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 16:28
 */
@XmlRootElement
public class NessusReportHost {

    private NessusHostProperties nessusHostProperties = new NessusHostProperties();
    private List<NessusReportItem> nessusReportItems = new ArrayList<NessusReportItem>();
    private String name = "";

    @XmlElement
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @XmlElement
    public NessusHostProperties getNessusHostProperties() {
        return nessusHostProperties;
    }

    public void setNessusHostProperties(NessusHostProperties nessusHostProperties) {
        this.nessusHostProperties = nessusHostProperties;
    }

    @XmlElement
    public List<NessusReportItem> getNessusReportItems() {
        return nessusReportItems;
    }

    public void setNessusReportItems(List<NessusReportItem> nessusReportItems) {
        this.nessusReportItems = nessusReportItems;
    }

    public void addNessusReportItem(NessusReportItem item) {
        this.nessusReportItems.add(item);
    }
}
