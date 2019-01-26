import graphitesend
import sys
import time
import datetime

sys.path.append('.')
import settings
import netflix_metrics

graphitesend.init(
    init_type='plaintext_tcp',
    graphite_server=settings.CARBON_SERVER,
    graphite_port=settings.CARBON_PORT,
    prefix=settings.CARBON_PREFIX,
    suffix=settings.CARBON_SUFFIX,
    system_name=settings.CARBON_SYSTEM,
)

current_timestamp = int(time.time())


def send_data(data, country_acr, prefix, message_postfix, api_type):
    """Send received data to carbon

    :param data: response of Metrological API in json
    :param country_acr: country acronym
    :param prefix: message prefix
    :param message_postfix: message postfix
    :param api_type: type of api (section)
    :return: pass
    """
    if api_type == 'widget':
        categories = data["data"][country_acr]["categories"]
        data_type = data["data"][country_acr]["data"]

        for i in range(0, len(categories)):
            tmp = categories[i] / 1000 + settings.TIME_SHIFT
            message = prefix + message_postfix
            print(message, data_type[i], datetime.datetime.fromtimestamp(tmp).isoformat())
            graphitesend.send(
                metric=message,
                value=data_type[i],
                timestamp=tmp,
            )
    else:
        avg = data["avg"]

        message = prefix + message_postfix
        print(message, avg, datetime.datetime.fromtimestamp(current_timestamp).isoformat())
        graphitesend.send(
            metric=message,
            value=avg,
            timestamp=current_timestamp,
            )
    pass


instance = netflix_metrics.Metro(settings.url_api, 'widgets', 'allowedApps', token=settings.token)
app_id_json = instance.get_allowed_apps_id()
list_apps_id = [app_id_json['apps'][n]['id'] for n in range(len(app_id_json))]

for acr, country_id in settings.country_acr.items():
    # prefix may be extended for other apps
    metrics_prefix = 'netflix.country.' + acr + '.metrological.'

    for metric_name, metric_property in settings.metric.items():
        if 'list apps id is required' in metric_property:
            for app_id in list_apps_id:
                instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, country_id,
                                                 settings.timespan[2], settings.timespan_options,
                                                 settings.template_type,
                                                 app_id, settings.token)
                print(instance.widget_call_api())
                # send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1], metric_property[0])

        # elif metric_property == 'widget':
        elif 'timestamp_lastweek':
            instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, country_id,
                                             settings.timespan[3], settings.timespan_options, settings.template_type,
                                             settings.app_id, settings.token)
            print(instance.widget_call_api())
            # send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1], metric_property[0])

        else:
            instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, country_id,
                                             settings.timespan[2], settings.timespan_options, settings.template_type,
                                             settings.app_id, settings.token)
            print(instance.widget_call_api())
            # send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1], metric_property[0])

        # elif metric_property[0] == 'applications':
        #     instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, acr,
        #                                      settings.timespan[0], settings.timespan_options, settings.template_type,
        #                                      settings.app_id, settings.token)
        #
        #     # get info just for Netflix, may be extended for other apps
        #     print([block for block in instance.application_call_api() if block['name'] == 'Netflix'])
        #
        #     # send_data(block, acr, metrics_prefix, metric_property[1], metric_property[0])

