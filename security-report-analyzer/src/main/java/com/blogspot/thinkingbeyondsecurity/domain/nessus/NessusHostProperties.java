package com.blogspot.thinkingbeyondsecurity.domain.nessus;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

/**
 * (c) Liquid Code Security
 * Date: 30.03.13
 * Time: 16:30
 */
@XmlRootElement
public class NessusHostProperties {

    private String hostEnd;
    private String systemType;
    private String operatingSystem;
    private String macAddress;
    private String hostIp;
    private String hostFQDN;
    private String netbiosName;
    private String hostStart;

    @XmlElement
    public String getHostEnd() {
        return hostEnd;
    }

    public void setHostEnd(String hostEnd) {
        this.hostEnd = hostEnd;
    }

    @XmlElement
    public String getSystemType() {
        return systemType;
    }

    public void setSystemType(String systemType) {
        this.systemType = systemType;
    }

    @XmlElement
    public String getOperatingSystem() {
        return operatingSystem;
    }

    public void setOperatingSystem(String operatingSystem) {
        this.operatingSystem = operatingSystem;
    }

    @XmlElement
    public String getMacAddress() {
        return macAddress;
    }

    public void setMacAddress(String macAddress) {
        this.macAddress = macAddress;
    }

    @XmlElement
    public String getHostIp() {
        return hostIp;
    }

    public void setHostIp(String hostIp) {
        this.hostIp = hostIp;
    }

    @XmlElement
    public String getHostFQDN() {
        return hostFQDN;
    }

    public void setHostFQDN(String hostFQDN) {
        this.hostFQDN = hostFQDN;
    }

    @XmlElement
    public String getNetbiosName() {
        return netbiosName;
    }

    public void setNetbiosName(String netbiosName) {
        this.netbiosName = netbiosName;
    }

    @XmlElement
    public String getHostStart() {
        return hostStart;
    }

    public void setHostStart(String hostStart) {
        this.hostStart = hostStart;
    }
}
