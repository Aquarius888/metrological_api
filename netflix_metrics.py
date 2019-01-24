import requests


class Metro(object):

    def __init__(self, url_api='', api_type='', metric='', country_id='', timespan='',
                 timespan_options='', template_type='', app_id='', token='', authorization=''):
        """

        :param url_api: from settings.py
        :param api_type: key of metric dict from settings.py
        :param metric: name of metric - first value in list of properties of metric dict from settings.py
        :param country_id: country id, matches are in metrological_exec.py
        :param timespan: list of strings timespan format
        :param timespan_options: encoded char {}
        :param template_type: string
        :param app_id: application Id
        :param token: token
        """
        self.token = token
        self.country_id = country_id
        self.url_api = url_api
        self.api_type = api_type
        self.metric = metric
        self.app_id = app_id
        self.timespan = timespan
        self.timespan_options = timespan_options
        self.template_type = template_type
        self.authorization = authorization

    def widget_call_api(self):
        """Make a request, widget metric.

        :return: response in json
        """
        complete_url = \
            '{0}/{1}/{2}?clientCountryId={3}&timespan={4}&timespanOptions={5}&templateType={6}&appId={7}'.\
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan, self.timespan_options,
                       self.template_type, self.app_id)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token,
                                                       'Authorization': 'Baerer ' + self.authorization})
        return response.json()

    def application_call_api(self):
        """Make a request, application section.

        :return: response in json
        """
        complete_url = \
            '{0}/{1}/{2}?operator=liberty&country={3}&environment=wpe-production&timespan={4}'.\
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token,
                                                       'Authorization': 'Baerer ' + self.authorization})
        return response.json()

    def get_allowed_apps_id(self):
        """Make a request, extract a list ID of allowed applications

        :return: response in json
        """
        complete_url = '{0}/{1}/{2}'.format(self.url_api, self.api_type, self.metric)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token,
                                                       'Authorization': 'Baerer ' + self.authorization})
        response.headers
        return response.json()



