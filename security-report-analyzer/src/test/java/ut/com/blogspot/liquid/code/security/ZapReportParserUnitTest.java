package ut.com.blogspot.liquid.code.security;

import com.atlassian.jira.issue.IssueInputParameters;
import com.blogspot.thinkingbeyondsecurity.domain.zap.ZapReportParser;
import org.junit.Test;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.util.List;

import static org.junit.Assert.*;

/**
 * (c) Liquid Code Security
 * Date: 09.04.13
 * Time: 18:48
 */
public class ZapReportParserUnitTest {

    @Test
    public void testParseFile() throws ParserConfigurationException, IOException, SAXException {
        // setting up mock and test data
        ZapReportParser zapReportParser = new ZapReportParser();

        Document xml = null;
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setValidating(false);
        factory.setNamespaceAware(false);
        DocumentBuilder builder = factory.newDocumentBuilder();

        File file = new File("src/test/resources_test/zaptestreport.xml");
        xml = builder.parse(file);

        // actual method call
        List<IssueInputParameters> result = zapReportParser.parse(xml);

        // asserts
        assertTrue(result.size() == 4);

        for (IssueInputParameters param : result) {

            if (param.getSummary().contains("Cross Site Request Forgery : http://192.168.56.101/")) {
                // assertEquals("Priority not equal", "HIGH", param.getPriorityId());
                assertNotNull("Description is null", param.getDescription());
            } else if (param.getSummary().contains("X-Content-Type-Options header missing : http://192.168.56.101/")) {
                // assertEquals("Priority not equal", "MEDIUM", param.getPriorityId());
                assertNotNull("Description is null", param.getDescription());
            } else if (param.getSummary().contains("X-Frame-Options not set : http://192.168.56.101/")) {
                // assertEquals("Priority not equal", "LOW", param.getPriorityId());
                assertNotNull("Description is null", param.getDescription());
            } else if (param.getSummary().contains("Cross Site Request Forgery : http://192.168.56.101/cgi-bin/badstore.cgi=action=supplierlogin")) {
                // assertEquals("Priority not equal", "HIGH", param.getPriorityId());
                assertNotNull("Description is null", param.getDescription());
            } else if (param.getSummary().contains("X-Frame-Options header not set : http://192.168.56.101/")) {
                // assertEquals("Priority not equal", "LOW", param.getPriorityId());
            } else {
                fail("Unknown Issue or not a bug : Summary: " + param.getSummary());
            }
        }
    }
}
