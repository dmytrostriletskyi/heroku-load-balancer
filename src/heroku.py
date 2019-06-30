"""
Provide implements of the Heroku domain.
"""
import requests


class HerokuApi:
    """
    Implements Heroku API communicator.
    """

    def __init__(self, key: str):
        """
        Constructor.
        """
        self.headers = {
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': f'Bearer {key}',
        }

    def fetch_pipeline_applications(self, identifier: str):
        """
        Fetch a pipeline applications by its identifier.
        """
        fetch_pipeline_applications_url = f'https://api.heroku.com/pipelines/{identifier}/pipeline-couplings'

        response = requests.get(fetch_pipeline_applications_url, headers=self.headers)
        response_json = response.json()

        return response_json

    def fetch_application(self, identifier: str):
        """
        Fetch an application by its identifier.
        """
        fetch_pipeline_applications_url = f'https://api.heroku.com/apps/{identifier}'

        response = requests.get(fetch_pipeline_applications_url, headers=self.headers)
        response_json = response.json()

        return response_json


class GetHerokuPipelineProductionApplicationsUrls:
    """
    Implement getting Heroku's pipeline production applications' URLs transaction.
    """

    def __init__(self, heroku_api: HerokuApi):
        """
        Constructor.
        """
        self.heroku_api = heroku_api

    def by_pipeline_identifier(self, identifier):
        """
        Get Heroku's pipeline production applications' URLs by pipeline identifier.
        """
        production_applications_identifiers = []

        for application in self.heroku_api.fetch_pipeline_applications(identifier=identifier):
            if application.get('stage') == 'production':
                application_identifier = application.get('app').get('id')
                production_applications_identifiers.append(application_identifier)

        production_applications_urls = []

        for application_identifier in production_applications_identifiers:
            application = self.heroku_api.fetch_application(identifier=application_identifier)
            application_url = application.get('web_url')
            production_applications_urls.append(application_url)

        return production_applications_urls
