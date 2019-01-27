import sys

sys.path.append('.')
import settings
import netflix_metrics
import graphite_delivery


# get list of allowed applications (id)
instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], 'allowedApps', token=settings.token)
app_id_json = instance.get_allowed()
list_apps_id = [app_id_json['apps'][n]['id'] for n in xrange(len(app_id_json))]

# get json of allowed widgets
instance = netflix_metrics.Metro(settings.url_api, settings.app_type[1], 'widgets-i-can-create', token=settings.token)
widgets_json = instance.get_allowed()

daily, realtime = 0, 0
daily_metrics, app_list_req = [], []
# realtime_metrics = []

# get lists of metrics
# change xrange to range if use python3
for n in xrange(len(widgets_json['widgets'])):
    if 'realtime' in widgets_json['widgets'][n]['tags'] and len(widgets_json['widgets'][n]['tags']) == 1:
        # print('widget:', widgets_json['widgets'][n]['widgetType'], ' : only realtime')
        # realtime_metrics.append(widgets_json['widgets'][n]['widgetType'])
        realtime += 1
    else:
        if 'last60mins' in widgets_json['widgets'][n]['createOptions']['timespan']:
            # print('widget:', response_json['widgets'][n]['widgetType'], ' : last60mins')
            daily += 1
            daily_metrics.append(widgets_json['widgets'][n]['widgetType'])
            if 'app' in widgets_json['widgets'][n]['tags']:
                app_list_req.append(widgets_json['widgets'][n]['widgetType'])


for acr, country_id in settings.country_acr.items():
    # prefix may be extended for other apps
    metrics_prefix = 'netflix.country.' + acr + '.metrological.'

    for metric_name in daily_metrics:
        if metric_name in app_list_req:
            for app_id in list_apps_id:
                instance = netflix_metrics.Metro(settings.url_api, settings.app_type[0], metric_name, country_id,
                                                 settings.timespan[0], settings.timespan_options,
                                                 settings.template_type,
                                                 app_id, settings.token)
                print(instance.widget_call_api())
                # graphite_delivery.send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1],
                # metric_property[0])
        else:
            instance = netflix_metrics.Metro(settings.url_api, settings.app_type[0], metric_name, country_id,
                                             settings.timespan[0], settings.timespan_options,
                                             settings.template_type,
                                             settings.app_id, settings.token)
            print(instance.widget_call_api())
            # graphite_delivery.send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1],
            # metric_property[0])

    # for metric_name, metric_property in settings.metric.items():
    #     if 'list apps id is required' in metric_property:
    #         for app_id in list_apps_id:
    #             instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, country_id,
    #                                              settings.timespan[2], settings.timespan_options,
    #                                              settings.template_type,
    #                                              app_id, settings.token)
    #             print(instance.widget_call_api())
    #             # send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1], metric_property[0])
    #
    #     # elif metric_property == 'widget':
    #     elif 'timestamp_lastweek':
    #         instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, country_id,
    #                                          settings.timespan[3], settings.timespan_options, settings.template_type,
    #                                          settings.app_id, settings.token)
    #         print(instance.widget_call_api())
    #         # send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1], metric_property[0])
    #
    #     else:  # timespan is last60mins
    #         instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, country_id,
    #                                          settings.timespan[2], settings.timespan_options, settings.template_type,
    #                                          settings.app_id, settings.token)
    #         print(instance.widget_call_api())
    #         # send_data(instance.widget_call_api(), acr, metrics_prefix, metric_property[1], metric_property[0])

        # elif metric_property[0] == 'applications':
        #     instance = netflix_metrics.Metro(settings.url_api, metric_property[0], metric_name, acr,
        #                                      settings.timespan[0], settings.timespan_options, settings.template_type,
        #                                      settings.app_id, settings.token)
        #
        #     # get info just for Netflix, may be extended for other apps
        #     print([block for block in instance.application_call_api() if block['name'] == 'Netflix'])
        #
        #     # send_data(block, acr, metrics_prefix, metric_property[1], metric_property[0])

