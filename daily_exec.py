from gevent import monkey
monkey.patch_socket()
monkey.patch_ssl()

import time
# import graphitesend
import datetime

# extend ulimit opened files
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

import sys
sys.path.append('.')
import settings
import netflix_metrics


current_timestamp = int(time.time())

# graphitesend.init(
#    init_type='plaintext_tcp',
#    graphite_server=settings.CARBON_SERVER,
#    graphite_port=settings.CARBON_PORT,
#    prefix=settings.CARBON_PREFIX,
#    suffix=settings.CARBON_SUFFIX,
#    system_name=settings.CARBON_SYSTEM,
# )


def get_list_of_urls():
    # get list of allowed applications (id)
    instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], 'allowedApps', token=settings.token,
                                     proxies=settings.proxy)
    app_id_json = instance.get_allowed()
    list_apps_id = [app_id_json['apps'][n]['id'] for n in xrange(len(app_id_json['apps']))
                    if ('test' and 'example') not in app_id_json['apps'][n]['id'].lower()]

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
            realtime += 1
        elif 'last60mins' in widgets_json['widgets'][n]['createOptions']['timespan']:
            daily += 1
            daily_metrics.append(widgets_json['widgets'][n]['widgetType'])
            if 'app' in widgets_json['widgets'][n]['tags']:
                app_list_req.append(widgets_json['widgets'][n]['widgetType'])
            else:
                netflix_metrics.configure_logging(settings.loglevel).debug(widgets_json['widgets'][n]['widgetType'],
                                                            widgets_json['widgets'][n]['createOptions']['timespan'])

    # get list of urls
    for acr, country_id in settings.country_acr.items():
        for metric_name in daily_metrics:
            if metric_name in app_list_req:
                for app_id in list_apps_id:
                    #daily timespan - last60mins
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

    return list_of_urls


def send_data(urls_list):
    for r in netflix_metrics.get_response_list(settings.token, settings.proxy, urls_list, timeout=15, size=16,
                                               exception_handler=netflix_metrics.exception_handler):
        if r.status_code == 200:
            acr, metric, applid = netflix_metrics.get_message(r.url, settings.country_acr)

            to_graphite(r.json(), settings.prefix, acr, metric, applid)


def to_graphite(data, prefix, country_acr, metric_name, applid):
    """Send received data to Graphite
    :param data: response of Metrological API in json
    :param prefix: prefix' format for graphite
    :param country_acr: country acronym
    :param metric_name: name of metric
    :param applid: application id, if it is required
    :return: pass
    """
    if 'categories' in data["data"][country_acr] and data["data"][country_acr]["categories"] != [] \
        and isinstance(data["data"][country_acr]["categories"][0], (int, float)):

        categories = data["data"][country_acr]["categories"]
        data_type = data["data"][country_acr]["data"]

        for i in xrange(0, len(categories)):
            tmp = categories[i] / 1000 + settings.TIME_SHIFT
            if applid == '':
                applid = 'general'
            if data_type[i] is None:
                continue
            message = '{0}.{1}.{2}.{3}'.format(prefix, country_acr, metric_name, applid)
            print(message, data_type[i], tmp)

            # graphitesend.send(
            #    metric=message,
            #    value=data_type[i],
            #    timestamp=tmp,
            # )
            
    elif country_acr in data["data"] and'categories' in data["data"][country_acr] \
        and data["data"][country_acr]["categories"] != [] \
        and not isinstance(data["data"][country_acr]["categories"][0], (int, float)):

        categories = data["data"][country_acr]["categories"]
        data_type = data["data"][country_acr]["data"]

        for i in xrange(len(categories)):
            message = '{0}.{1}.{2}.{3}'.format(prefix, country_acr, metric_name, categories[i])
            print(message, data_type[i], current_timestamp)

            # graphitesend.send(
            #    metric=message,
            #    value=data_type[i],
            #    timestamp=current_timestamp,
            # )

    elif country_acr in data["data"] and 'data' in data["data"][country_acr]:
        data_type = data["data"][country_acr]["data"]

        for i in xrange(len(data_type)):
            message = '{0}.{1}.{2}.{3}'.format(prefix, country_acr, metric_name, data_type[i]['name'].encode('ascii', 'ignore'))
            print(message, data_type[i]['data'], current_timestamp)

            # graphitesend.send(
            #    metric=message,
            #    value=int(data_type[i]['data']),
            #    timestamp=current_timestamp,
            # )


if __name__ == "__main__":
    netflix_metrics.configure_logging(settings.loglevel).info('RUN.........')
    list_of_urls = get_list_of_urls()
    send_data(list_of_urls)
    netflix_metrics.configure_logging(settings.loglevel).info('FINISH.........')

