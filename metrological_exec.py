import graphitesend
import sys
import time
import datetime

sys.path.append('.')
import settings
import netflix_metrics

# graphitesend.init(
#     init_type='plaintext_tcp',
#     graphite_server=settings.CARBON_SERVER,
#     graphite_port=settings.CARBON_PORT,
#     prefix=settings.CARBON_PREFIX,
#     suffix=settings.CARBON_SUFFIX,
#     system_name=settings.CARBON_SYSTEM,
# )

current_timestamp = int(time.time())
# country_acr = ['nl', 'de', 'ch', 'ie']


def send_data(data, country_acr, prefix, message_postfix, api_type):
    if api_type == 'widget':
        categories = data["data"][country_acr]["categories"]
        data_type = data["data"][country_acr]["data"]

        for i in range(0, len(categories)):
            tmp = categories[i] / 1000 + settings.TIME_SHIFT
            message = prefix + message_postfix
            print(message, data_type[i], datetime.datetime.fromtimestamp(tmp).isoformat())
            # graphitesend.send(
            #     metric=message,
            #     value=data_type[i],
            #     timestamp=tmp,
            # )
    else:
        avg = data["avg"]

        message = prefix + message_postfix
        print(message, avg, datetime.datetime.fromtimestamp(current_timestamp).isoformat())
        # graphitesend.send(
        #     metric=message,
        #     value=avg,
        #     timestamp=current_timestamp,
        #     )
    pass


for arg in settings.country_acr:
    metrics_prefix = 'netflix.country.' + arg + '.metrological.'

    if arg == "nl":
        country_id = 1
    elif arg == "de":
        country_id = 2
    elif arg == "ch":
        country_id = 3
    elif arg == "ie":
        country_id = 4

    # get widget/app_time_spend
    for metric_name, value in settings.metric.items():
        print(metric_name, value)

        if value[0] == 'widget':
            instance = netflix_metrics.Metro(settings.url_api, value[0], metric_name, country_id,
                                             settings.timespan[1], settings.timespan_options, settings.template_type,
                                             settings.app_id)
            print(instance.widget_call_api())
        elif value[0] == 'applications':
            instance = netflix_metrics.Metro(settings.url_api, value[0], metric_name, arg,
                                             settings.timespan[0], settings.timespan_options, settings.template_type,
                                             settings.app_id)
            print(instance.application_call_api())

    # send_data(instance.widget_call_api(), arg, metrics_prefix, settings.metric.get('app_time_spend'),
    #           settings.api_type[0])
