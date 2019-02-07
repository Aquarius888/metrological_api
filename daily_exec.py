import sys
import os
import logging
from logging.handlers import RotatingFileHandler

from gevent import monkey
monkey.patch_socket()

# import graphitesend
import datetime

# extend ulimit opened files
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

sys.path.append('.')
import settings
import netflix_metrics


# graphitesend.init(
#    init_type='plaintext_tcp',
#    graphite_server=settings.CARBON_SERVER,
#    graphite_port=settings.CARBON_PORT,
#    prefix=settings.CARBON_PREFIX,
#    suffix=settings.CARBON_SUFFIX,
#    system_name=settings.CARBON_SYSTEM,
# )


def configure_logging():
    logger = logging.getLogger(__name__)
    level = getattr(logging, settings.loglevel)
    logger.setLevel(level)
    format_str = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt=format_str)

    script_name = os.path.basename(__file__).split(".")[0]
    log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '{0}.log'.format(script_name))
    rotating_hndlr = RotatingFileHandler(filename=log_path, maxBytes=5*1024*1024, backupCount=2)
    rotating_hndlr.setFormatter(formatter)
    logger.addHandler(rotating_hndlr)

    return logger


def get_list_of_urls():
    # get list of allowed applications (id)
    instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], 'allowedApps', token=settings.token,
                                     proxies=settings.proxy)
    app_id_json = instance.get_allowed()
    list_apps_id = [app_id_json['apps'][n]['id'] for n in xrange(len(app_id_json['apps']))
                    if 'test' not in app_id_json['apps'][n]['id'].lower()]

    # get json of allowed widgets
    instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], 'widgets-i-can-create',
                                     token=settings.token, proxies=settings.proxy)
    widgets_json = instance.get_allowed()

    daily, realtime = 0, 0
    daily_metrics, app_list_req, list_of_urls = [], [], []

    # get lists of metrics
    # change xrange to range if use python3
    for n in xrange(len(widgets_json['widgets'])):
        if 'realtime' in widgets_json['widgets'][n]['tags'] and len(widgets_json['widgets'][n]['tags']) == 1:
            configure_logging().debug('widget: {}: only realtime'.format(
                                                        widgets_json['widgets'][n]['widgetType']))
            realtime += 1
        elif 'last60mins' in widgets_json['widgets'][n]['createOptions']['timespan']:
            configure_logging().debug('widget: {}: last60mins'.format(
                                                        widgets_json['widgets'][n]['widgetType']))
            daily += 1
            daily_metrics.append(widgets_json['widgets'][n]['widgetType'])
            if 'app' in widgets_json['widgets'][n]['tags']:
                app_list_req.append(widgets_json['widgets'][n]['widgetType'])
            else:
                configure_logging().debug(widgets_json['widgets'][n]['widgetType'],
                                                            widgets_json['widgets'][n]['createOptions']['timespan'])

    for acr, country_id in settings.country_acr.items():
        for metric_name in daily_metrics:
            if metric_name in app_list_req:
                for app_id in list_apps_id:
                    instance = netflix_metrics.Metro(settings.url_api, settings.app_type[0], metric_name, country_id,
                                                     settings.timespan[0], settings.timespan_options,
                                                     settings.template_type, settings.token, settings.proxy, app_id)
                    list_of_urls.append(instance.get_list_of_url())
            else:
                instance = netflix_metrics.Metro(settings.url_api, settings.app_type[0], metric_name, country_id,
                                                 settings.timespan[0], settings.timespan_options,
                                                 settings.template_type,
                                                 settings.token, settings.proxy, app_id='')
                list_of_urls.append(instance.get_list_of_url())
    configure_logging().debug('Daily metrics: {0}. Application required: {1}'.
                                               format(len(daily_metrics), len(app_list_req)))
    return list_of_urls


def send_data(urls_list):
    success = 0
    for r in netflix_metrics.get_response_list(settings.token, settings.proxy, urls_list, timeout=15, size=16,
                                               exception_handler=netflix_metrics.exception_handler):
        if r.status_code == 200:
            success += 1
            acr, metric, applid = netflix_metrics.get_message(r.url, settings.country_acr)
            # configure_logging().debug(netflix_metrics.get_message(r.url, settings.country_acr))

            to_graphite(r.json(), acr, metric, applid)

    configure_logging().info('Amount of requests: {0}, successfully responds: {1}'.format(len(urls_list), success))


def to_graphite(data, country_acr, metric_name, applid=''):
    """Send received data to Graphite
    :param data: response of Metrological API in json
    :param country_acr: country acronym
    :param metric_name: name of metric
    :param applid: application id, if it is required
    :return: pass
    """
    if 'categories' in data["data"][country_acr] and data["data"][country_acr]["categories"] != [] and \
        isinstance(data["data"][country_acr]["categories"][0], int):

        categories = data["data"][country_acr]["categories"]
        data_type = data["data"][country_acr]["data"]

        for i in xrange(0, len(categories)):
            tmp = categories[i] / 1000 + settings.TIME_SHIFT
            message = 'metrological.country.{0}.{1}.{2}'.format(country_acr, metric_name, applid)
            print(message, data_type[i], datetime.datetime.fromtimestamp(tmp).isoformat())
            # configure_logging().debug((message, data_type[i], datetime.datetime.fromtimestamp(tmp).isoformat()))
            # graphitesend.send(
            #    metric=message,
            #    value=data_type[i],
            #    timestamp=tmp,
            # )


if __name__ == "__main__":
    configure_logging().info('RUN.........')
    list_of_urls = get_list_of_urls()
    send_data(list_of_urls)
    configure_logging().info('FINISH.........')
