import json
import sys
import requests
import urllib3


class SonarAPIClient:
    def __init__(self, url, configuration):
        """
        Constructor
        :param url: to generate http-connection to
        """
        self.main_url = url
        self.main_config = configuration
        self._session = requests.Session()
        self._session.verify=False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return

    def make_apicall(self, method, apistring, tokenId):
        """
        Call Rest API of SONAR for report.
        :param method:
        :param apistring:
        :return: response as JSON Object
        """
        
        token = str(self.main_config['creds'][tokenId])
        self._session.auth = token, ''
        
        url = str(self.main_url) + apistring
        call = getattr(self._session, method.lower())
        response = call(url)

        #TODO handle status code != 200
        
        data = json.loads(response.text)
        return data

    @staticmethod
    def write_statusmessage(self, message, i, maximum):
        """
        Write status message to standard out
        :param self: self
        :param message: message to log
        :param i: counter variable
        :param maximum: second counter variable
        :return: NONE
        """
        message_string = ""
        message_string += message

        if i:
            message_string += " " + str(i)

        if maximum:
            message += " " + str(maximum)

        sys.stdout.write('\r ' + message)
        sys.stdout.flush()
        return

    @staticmethod
    def __extract_by_key__(self, source, destination, key):
        """
        Extract Object form List of Object by Key
        :param self: self
        :param source: data source to extract values from
        :param destination: data sink to store extracted data in
        :param key: key to look for to extract values
        :return: none - destination will be updated
        """
        if key in source:
            if source[key]:
                if isinstance(source[key],  list):
                    for element in source[key]:
                        destination.append(element)
                else:
                    destination.append(source[key])

    def search_issues(self, install_name, type_to_search, status, resolutions):
        """
        :param self: self
        :param type_to_search: Type of issue to search for
        :param install_name: prefix to be used in url to identify sonaqube installation
        :param status: the status the issues should be in
        :param resolutions: resolution of issues to search
        :return: array of issues found for this type
        """

        url = install_name + "/api/issues/search?"
        tokenId = None;
        if install_name == "":
            tokenId = "all"
        else:
            tokenId = str(install_name)[1:]
            
        if status:
           url += "statuses="+ status
        if type_to_search:
            url += "&types=" + type_to_search
        if resolutions:
            url += "&resolutions=" + resolutions

        issues = []
        
        service_answer = self.make_apicall("GET", url, tokenId)
        self.__extract_by_key__(self, service_answer, issues, "issues")

        if 'total' in service_answer and service_answer['total'] > 1:
            p = 1
            while p < service_answer['total']:
                p += 1
                url2 = url + "&p=" + str(p)
                service_answer2 = self.make_apicall("GET", url2, tokenId)
                self.__extract_by_key__(self, service_answer2, issues, "issues")

        return issues
