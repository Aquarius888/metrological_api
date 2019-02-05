"""
Redesign it for weekly usage; implement selection only weekly metrics
"""

import sys
# import json
# import requests

# extend ulimit opened files
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

sys.path.append('.')
import settings
import netflix_metrics
import graphite_delivery


# get list of allowed applications (id)
instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], 'allowedApps', token=settings.token)
app_id_json = instance.get_allowed()
list_apps_id = [app_id_json['apps'][n]['id'] for n in xrange(len(app_id_json['apps'])) if 'test' not in
                app_id_json['apps'][n]['id'].lower()]

# get json of allowed widgets
instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], 'widgets-i-can-create', token=settings.token)
widgets_json = instance.get_allowed()

daily, realtime = 0, 0
daily_metrics, app_list_req, list_of_urls = [], [], []

# get lists of metrics
# change xrange to range if use python3
for n in xrange(len(widgets_json['widgets'])):
    if 'realtime' in widgets_json['widgets'][n]['tags'] and len(widgets_json['widgets'][n]['tags']) == 1:
        # graphite_delivery.configure_logging().debug('widget:', widgets_json['widgets'][n]['widgetType'],
        # ' : only realtime')
        realtime += 1
    else:
        if 'lastweek' in widgets_json['widgets'][n]['createOptions']['timespan']:
            # graphite_delivery.configure_logging().debug('widget:', response_json['widgets'][n]['widgetType'],
            # ' : last60mins')
            daily += 1
            daily_metrics.append(widgets_json['widgets'][n]['widgetType'])
            if 'app' in widgets_json['widgets'][n]['tags']:
                app_list_req.append(widgets_json['widgets'][n]['widgetType'])
        # else:
            # graphite_delivery.configure_logging().debug(widgets_json['widgets'][n]['widgetType'], ' ===> ',
        # widgets_json['widgets'][n]['createOptions']['timespan'])

# graphite_delivery.configure_logging().debug(daily, daily_metrics)
# graphite_delivery.configure_logging().debug(len(app_list_req), app_list_req)


for acr, country_id in settings.country_acr.items():
    for metric_name in daily_metrics:
        if metric_name in app_list_req:
            for app_id in list_apps_id:
                instance = netflix_metrics.Metro(settings.url_api, settings.app_type[0], metric_name, country_id,
                                                 settings.timespan[1], settings.timespan_options,
                                                 settings.template_type,
                                                 app_id, settings.token)
                list_of_urls.append(instance.get_list_of_url())
        else:
            instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], metric_name, country_id,
                                             settings.timespan[0], settings.timespan_options,
                                             settings.template_type,
                                             settings.app_id, settings.token)
            list_of_urls.append(instance.get_list_of_url())


success = 0

for r in netflix_metrics.get_response_list(settings.token, list_of_urls, timeout=15, size=16,
                                           exception_handler=graphite_delivery.exception_handler):
    if r.status_code == 200:
        # graphite_delivery.configure_logging().debug(r.status_code, r.url)
        success += 1
        # first step to graphite_send_data
        acr, metric, applid = netflix_metrics.get_message(r.url, settings.country_acr)
        graphite_delivery.configure_logging().debug(netflix_metrics.get_message(r.url, settings.country_acr))
        # graphite_delivery.send_data(r.json(), settings.api_type[0], acr, metric, applid=applid)
graphite_delivery.configure_logging().debug(len(list_of_urls), success)
