import requests


class Metro:

    def __init__(self, url_api, proxies, headers):
        self.url_api = url_api
        self.session = requests.Session()
        self.session.headers = headers
        self.session.proxies = proxies

    def get_allowed(self, api_type, metric):
        compose_url = '{0}/{1}/{2}'.format(self.url_api, api_type, metric)
        r = self.session.get(compose_url)
        return r.json()

    @staticmethod
    def get_country_str(country_dict):
        country_list = ['clientCountryId={}'.format(country_id) for acr, country_id in country_dict.items()]
        return '&'.join(country_list)

    @staticmethod
    def get_metric_list(w_json, timespan):
        daily_metrics, weekly_metrics, app_list_req, weekly_app_list_req = [], [], [], []
        widg = w_json['widgets']
        lasthour = 'last60mins'

        # change xrange to range if use python3
        for n in xrange(len(widg)):
            w_type = widg[n]['widgetType']
            if 'realtime' in widg[n]['tags'] and len(widg[n]['tags']) == 1:
                continue

            elif lasthour in widg[n]['createOptions']['timespan']:
                daily_metrics.append(w_type)
                if 'app' in widg[n]['tags']:
                    app_list_req.append(w_type)
            else:
                weekly_metrics.append(w_type)
                if 'app' in widg[n]['tags']:
                    weekly_app_list_req.append(w_type)

        if timespan is lasthour:
            return daily_metrics, app_list_req
        else:
            return weekly_metrics, weekly_app_list_req

    def get_url(self, api_type, metric, country_id, timespan, timespan_options, template_type, app_id):
        complete_url = \
            '{0}/{1}/{2}?{3}&timespan={4}&timespanOptions={5}&templateType={6}&appId={7}'. \
                format(self.url_api, api_type, metric, country_id, timespan, timespan_options, template_type, app_id)

        return complete_url

    def get_response(self, url):
        response = self.session.get(url)
        return response

    @staticmethod
    def get_message(url):
        """
        Parse url, extract and prepare widget name and application name
        :param url:
        :return: prepared widget name, appropriated application name
        """
        lst = [i.split('=')[1] for i in url.split('?')[1].split('&')]
        widget = url.split('?')[0].split('/')[-1]
        app_id = lst[-1].split('.')
        return ''.join([part.capitalize() for part in widget.split('_')]), \
               ''.join([part.capitalize() for part in app_id[1:]])
