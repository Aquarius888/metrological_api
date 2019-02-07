import requests
import grequests


class Metro(object):

    def __init__(self, url_api='', api_type='', metric='', country_id='', timespan='',
                 timespan_options='', template_type='', token='', proxies='', app_id=''):
        """
        :param url_api: from settings.py
        :param api_type: key of metric dict from settings.py
        :param metric: name of metric - first value in list of properties of metric dict from settings.py
        :param country_id: country id, matches are in exec files
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
        self.proxies = proxies
        self.timespan = timespan
        self.timespan_options = timespan_options
        self.template_type = template_type

    def widget_call_api(self):
        """Make a request, widget metric.
        :return: response in json
        """
        complete_url = \
            '{0}/{1}/{2}?clientCountryId={3}&timespan={4}&timespanOptions={5}&templateType={6}&appId={7}'.\
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan, self.timespan_options,
                       self.template_type, self.proxies, self.app_id)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token}, proxies=self.proxies)
        return response.json()

    def application_call_api(self):
        """Make a request, application section.
        :return: response in json
        """
        complete_url = \
            '{0}/{1}/{2}?operator=liberty&country={3}&environment=wpe-production&timespan={4}'.\
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token}, proxies=self.proxies)
        return response.json()

    def get_allowed(self):
        """Make a request, extract a list of allowed applications or widgets
        :return: response in json
        """
        complete_url = '{0}/{1}/{2}'.format(self.url_api, self.api_type, self.metric)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token}, proxies=self.proxies)
        return response.json()

    def get_list_of_url(self):
        complete_url = \
            '{0}/{1}/{2}?clientCountryId={3}&timespan={4}&timespanOptions={5}&templateType={6}&appId={7}'. \
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan, self.timespan_options,
                       self.template_type, self.app_id)
        return complete_url


# catch an exception
def exception_handler(request, exception):
    print("Request failed", request.url)
    print(str(exception))


def get_response_list(token, proxies, list_of_urls, timeout=5, size=16, exception_handler=''):
    response_list = (grequests.get(url, headers={'X-Api-Token': token}, proxies=proxies, timeout=timeout)
                     for url in list_of_urls)
    return grequests.imap(response_list, size=size, exception_handler=exception_handler)


# get acronym, widget name, complited app id from url
def get_message(url, country_acr):
    lst = [i.split('=')[1] for i in url.split('?')[1].split('&')]
    acronym = [acr for acr, id in country_acr.items() if id == int(lst[0])][0]
    widget = url.split('?')[0].split('/')[-1]
    app_id = lst[-1].split('.')
    return acronym, ''.join([part.capitalize() for part in widget.split('_')]),\
           ''.join([part.capitalize() for part in app_id[1:]])
