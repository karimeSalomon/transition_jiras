import requests
import json
from requests.auth import HTTPBasicAuth
from helpers.config import Config


class GetFromJira:
    __instance = None

    @staticmethod
    def instance():
        """ Static access method. """
        if GetFromJira.__instance is None:
            GetFromJira()
        return GetFromJira.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if GetFromJira.__instance is not None:
            raise Exception("This class is a singleton!")
        else:

            GetFromJira.__instance = self
            self.config = Config.instance().data['credentials']
            self.headers = {"Content-Type": "application/json",
                            "Accept": "application/json"}
            self.version = 2
            self.email = self.config['email']
            self.jira_token = self.config['jira_token']
            self.server = self.config['server']

    def get(self, endpoint, body=None):
        """
        Performs GET method to SharePoint
        :param endpoint: Admin API endpoint or query
        :param body: Optional
        :return: Response of REST API
        """

        return requests.get('{server}/rest/api/{version}/{endpoint}'.format(server=self.config['server'],
                                                                            version=self.version,
                                                                            endpoint=endpoint),
                            headers=self.headers, data=body,
                            auth=HTTPBasicAuth(self.config['email'], self.config['jira_token']))

    def post(self, endpoint, body=None):
        """
        Performs POST method to Admin API
        :param endpoint: Admin API endpoint or query
        :param body: Payload or None as default value
        :return: Response of REST API
        """

        return requests.post('{server}/rest/api/{version}/{endpoint}'.format(server=self.server,
                                                                             version=self.version,
                                                                             endpoint=endpoint),
                             data=body, headers=self.headers,
                             auth=HTTPBasicAuth(self.email, self.jira_token))

    def get_id_from_project(self, project):
        """
                Performs GET method to JIRA project
                :param project: JIRA project key
                :return: project id
        """

        # Create a request object with above parameters.
        response = requests.request(
            "GET",
            self.server + "/rest/api/" + str(self.version) + "/project/" + project,
            headers=self.headers,
            auth=HTTPBasicAuth(self.email, self.jira_token)
        )

        # Get information of project by using the
        # json loads method.
        project_info = json.dumps(json.loads(response.text),
                                  sort_keys=True,
                                  indent=4,
                                  separators=(",", ": "))
        # The JSON response received, using
        # the requests object,
        # is an intricate nested object.
        # Convert the output to a dictionary object.
        dictproject_info = json.loads(project_info)

        # Will return the 'id' of the project
        return dictproject_info['id']

    def get_all_releases_from_project(self, id):
        """
                Performs GET method to JIRA project by id
                :param id: JIRA project id
                :return: JSON response converted to a dictionary
        """
        # Create a request object with above parameters.
        response = requests.request(
            "GET",
            self.server + "/rest/api/" + str(self.version) + "/project/" + id + "/versions",
            headers=self.headers,
            auth=HTTPBasicAuth(self.email, self.jira_token)
        )

        # Get all project issues,by using the
        # json loads method.
        release_dates = json.dumps(json.loads(response.text),
                                   sort_keys=True,
                                   indent=4,
                                   separators=(",", ": "))

        # The JSON response received, using
        # the requests object,
        # is an intricate nested object.
        # Convert the output to a dictionary object.
        dict_release_response = json.loads(release_dates)
        # print(dict_release_response)

        return dict_release_response
