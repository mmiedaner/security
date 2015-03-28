package ut.com.blogspot.liquid.code.security;

import com.atlassian.jira.issue.IssueInputParameters;
import com.blogspot.thinkingbeyondsecurity.domain.nessus.NessusReportParser;
import org.junit.Test;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.util.List;

import static org.junit.Assert.assertTrue;

/**
 * (c) Liquid Code Security
 * Date: 09.04.13
 * Time: 21:08
 */
public class NessusReportParserUnitTest {

    @Test
    public void testParseNessusReport() throws ParserConfigurationException, IOException, SAXException {
        // setting up mocks and testdata
        NessusReportParser nessusReportParser = new NessusReportParser();

        Document xml = null;
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setValidating(false);
        factory.setNamespaceAware(false);
        DocumentBuilder builder = factory.newDocumentBuilder();

        File file = new File("src/test/resources_test/nessustestreport.nessus");
        xml = builder.parse(file);

        // actual method call
        List<IssueInputParameters> result = nessusReportParser.parse(xml);

        System.out.println("Size: " + result.size());

        for (IssueInputParameters param : result) {
            System.out.println("Param: " + param.getSummary());
        }

        assertTrue(result.size() == 4);

    }
}
