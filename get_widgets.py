import requests
#import json
import sys
import os
import logging
from logging.handlers import RotatingFileHandler

sys.path.append('.')
import settings


def configure_logging():
    logger = logging.getLogger(__name__)
    logger.level = 1
    format_str = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt=format_str)

    script_name = os.path.basename(__file__).split(".")[0]
    log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '{0}.log'.format(script_name))
    rotating_hndlr = RotatingFileHandler(filename=log_path, maxBytes=5*1024*1024, backupCount=2)
    rotating_hndlr.setFormatter(formatter)
    logger.addHandler(rotating_hndlr)

    return logger


url = 'http://api-metrological/api/clientCountry/widgets/widgets-i-can-create'
response = requests.get(url, headers={'X-Api-Token': settings.token})
#print(response.reason, response.raw, response.url, response.headers)
response_json = response.json()

#print(response_json['widgets'][0]['widgetType'], response_json['widgets'][0]['createOptions']['timespan'])
#print([response_json['widgets'][n] for n in range(len(response_json['widgets'])) if 'total_widgets_created' in response_json['widgets'][n]['widgetType']])
#print([response_json['widgets'][n]['tags'] for n in range(len(response_json['widgets']))])

daily, weekly, realtime = 0, 0, 0
daily_metrics, weekly_metrics = [], []

# change xrange to range if use python3
for n in xrange(len(response_json['widgets'])):
    if 'realtime' in response_json['widgets'][n]['tags'] and len(response_json['widgets'][n]['tags']) == 1:
        print('widget:', response_json['widgets'][n]['widgetType'], ' : only realtime')
        realtime += 1
    else:
        if 'last60mins' in response_json['widgets'][n]['createOptions']['timespan']:
            # print('widget:', response_json['widgets'][n]['widgetType'], ' : last60mins')
            daily += 1
            daily_metrics.append(response_json['widgets'][n]['widgetType'])
        elif 'lastweek' in response_json['widgets'][n]['createOptions']['timespan']:
            # print('widget:', response_json['widgets'][n]['widgetType'], ' : lastweek')
            weekly += 1
            weekly_metrics.append(response_json['widgets'][n]['widgetType'])

#print('daily: {0}\n weekly: {1}\n realtime: {2}'.format(daily, weekly, realtime))
print(daily_metrics)
print(weekly_metrics)