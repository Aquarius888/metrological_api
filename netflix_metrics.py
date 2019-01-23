import json
import os
import time
import graphitesend
import datetime
import requests

url_api = 'https://api.metrological.com/api/clientCountry'
api_type = ['widget', 'applications']
metric = ['app_time_spend', 'app_time_spend', 'app_amount_opened']
token = '0c17b77af4c2a23165901a5110b1cd6989f7169a6155565bd9ecad53b8df06a7'
app_id = 'com.metrological.app.NetflixHorizon'
timespan = 'last7days'
timespan_options = '%7B%7D' #{}
template_type = 'line'


# CARBON_SERVER = '172.27.66.160'
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
CARBON_PREFIX = ''
CARBON_SUFFIX = ''
CARBON_SYSTEM = ''
current_timestamp = int(time.time())
# To compensate time shift between response from
# metrologic (UTC) and local server time (UTC+1(winter),+2(summer))
TIME_SHIFT = 7200

# graphitesend.init(
#     init_type='plaintext_tcp',
#     graphite_server=CARBON_SERVER,
#     graphite_port=CARBON_PORT,
#     prefix=CARBON_PREFIX,
#     suffix=CARBON_SUFFIX,
#     system_name=CARBON_SYSTEM,
# )

# for arg in ['nl', 'de', 'ch', 'ie']:
#     METRICS_PREFIX = 'netflix.country.' + arg + '.metrological.'
#
#     if arg == "nl":
#         country = 1
#     elif arg == "de":
#         country = 2
#     elif arg == "ch":
#         country = 3
#     elif arg == "ie":
#         country = 4


class Metro(object):

    def __init__(self, url_api='', api_type='', metric='', country_id='', timespan='',
                 timespan_options='', template_type='', app_id='', token=''):
        self.token = token
        self.country_id = country_id
        self.url_api = url_api
        self.api_type = api_type
        self.metric = metric
        self.app_id = app_id
        self.timespan = timespan
        self.timespan_options = timespan_options
        self.template_type = template_type

    def widget_call_api(self):
        complete_url = \
            '{0}/{1}/{2}?clientCountryId={3}&timespan={4}&timespanOptions={5}&templateType={6}&appId={7}'.\
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan, self.timespan_options,
                       self.template_type, self.app_id)
        # response = requests.get(complete_url, headers={'X-Api-Token': self.token})
        # return response.json()
        return complete_url

    def application_call_api(self):
        complete_url = \
            '{0}/{1}/{2}?clientCountryId={3}&timespan={4}&timespanOptions={5}&templateType={6}&appId={7}'.\
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan, self.timespan_options,
                       self.template_type, self.app_id)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token})
        return response.raise_for_status()

    def send_data(self):
        pass

country_id = '1'
instance = Metro(url_api, api_type[0], metric[0], country_id, timespan, timespan_options, template_type, app_id)
print(instance.application_call_api())
