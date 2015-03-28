package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.util.List;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 16:38
 */
@XmlRootElement
public class NessusPolicy {

    private String policyName;
    private List<NessusServerPolicy> nessusServerPolicies;
    private List<NessusPluginPolicy> nessusPluginPolicies;

    @XmlElement
    public String getPolicyName() {
        return policyName;
    }

    public void setPolicyName(String policyName) {
        this.policyName = policyName;
    }

    @XmlElement
    public List<NessusServerPolicy> getNessusServerPolicies() {
        return nessusServerPolicies;
    }

    public void setNessusServerPolicies(List<NessusServerPolicy> nessusServerPolicies) {
        this.nessusServerPolicies = nessusServerPolicies;
    }

    public void addNessusServerPolicy(NessusServerPolicy policy) {
        this.nessusServerPolicies.add(policy);
    }

    @XmlElement
    public List<NessusPluginPolicy> getNessusPluginPolicies() {
        return nessusPluginPolicies;
    }

    public void setNessusPluginPolicies(List<NessusPluginPolicy> nessusPluginPolicies) {
        this.nessusPluginPolicies = nessusPluginPolicies;
    }

    public void addNessusPluginPolicies(NessusPluginPolicy policy) {
        this.nessusPluginPolicies.add(policy);
    }
}
