import httplib
import json
import sys
import requests


class SonarAPIClient:
    def __init__(self, url):
        """
        Constructor
        :param url: to generate http-connection to
        """
        self.main_url = url
        self.connection = httplib.HTTPSConnection(self.main_url)
        return

    def make_apicall(self, method, apistring):
        """
        Call Rest API of SONAR for report.
        :param method:
        :param apistring:
        :return: response as JSON Object
        """
        response = requests.request(method, self.main_url + apistring, verify=False)
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
        if status:
           url += "statuses="+ status
        if type_to_search:
            url += "&types=" + type_to_search
        if resolutions:
            url += "&resolutions=" + resolutions

        issues = []
        service_answer = self.make_apicall("GET", url)
        self.__extract_by_key__(self, service_answer, issues, "issues")

        if 'total' in service_answer and service_answer['total'] > 1:
            p = 1
            while p < service_answer['total']:
                p += 1
                url2 = url + "&p=" + str(p)
                service_answer2 = self.make_apicall("GET", url2)
                self.__extract_by_key__(self, service_answer2, issues, "issues")

        return issues
