import json
import os
import time
import graphitesend
import datetime
import sys
import requests

# sys.path.append('.')
# import settings


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
        response = requests.get(complete_url, headers={'X-Api-Token': self.token})
        # return 'widget_call_api'
        return complete_url

    def application_call_api(self):
        complete_url = \
            '{0}/{1}/{2}?operator=liberty&country={3}&environment=wpe-production&timespan={4}'.\
                format(self.url_api, self.api_type, self.metric, self.country_id, self.timespan)
        response = requests.get(complete_url, headers={'X-Api-Token': self.token})
        # return 'application_call_api'
        return complete_url



