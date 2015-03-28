package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.util.ArrayList;
import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 27.03.13
 * Time: 16:56
 */

@XmlRootElement
public class NessusReport {

    private List<NessusPolicy> policies = new ArrayList<NessusPolicy>();
    private List<NessusReportHost> nessusReportHosts = new ArrayList<NessusReportHost>();

    @XmlElement
    public List<NessusPolicy> getPolicies() {
        return policies;
    }

    public void setPolicies(List<NessusPolicy> policies) {
        this.policies = policies;
    }

    public void addPoliciy(NessusPolicy policy) {
        this.policies.add(policy);
    }

    @XmlElement
    public List<NessusReportHost> getNessusReportHosts() {
        return nessusReportHosts;
    }

    public void setNessusReportHosts(List<NessusReportHost> nessusReportHosts) {
        this.nessusReportHosts = nessusReportHosts;
    }

    public void addNessusReportHost(NessusReportHost reportHost) {
        this.nessusReportHosts.add(reportHost);
    }
}
