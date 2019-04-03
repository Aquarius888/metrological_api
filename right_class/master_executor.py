import time
import graphitesend

import settings
import metrogenerator

###########################
current_timestamp = int(time.time())

graphitesend.init(
   init_type='plaintext_tcp',
   graphite_server=settings.CARBON_SERVER,
   graphite_port=settings.CARBON_PORT,
   prefix=settings.CARBON_PREFIX,
   suffix=settings.CARBON_SUFFIX,
   system_name=settings.CARBON_SYSTEM,
)

###########################

m = metrogenerator.Metro(settings.url_api, settings.proxy, settings.headers)

app_id_json = m.get_allowed(settings.app_type[1], 'allowedApps')

list_apps_id = [app_id_json['apps'][n]['id'] for n in xrange(len(app_id_json['apps']))
                if 'test' not in app_id_json['apps'][n]['id'].lower()
                and 'example' not in app_id_json['apps'][n]['id'].lower()]

widgets_json = m.get_allowed(settings.app_type[1], 'widgets-i-can-create')

daily_metrics, app_list_req = m.get_metric_list(widgets_json, settings.timespan[0])

non_req = list(set(daily_metrics) - set(app_list_req))

urls = [m.get_url(settings.app_type[0], metric_name, m.get_country_str(settings.country_acr),
                  settings.timespan[0], settings.timespan_options, settings.template_type, app_id='')
        for metric_name in non_req]

urls_app = [m.get_url(settings.app_type[0], metric_name, m.get_country_str(settings.country_acr),
                      settings.timespan[0], settings.timespan_options, settings.template_type, app_id)
            for metric_name in app_list_req for app_id in list_apps_id]

print(len(urls), len(urls_app))
urls.extend(urls_app)

execution = 0
###
for url in urls:
    resp = m.get_response(url)
    if resp.status_code == 200:
        m_name, app_name = m.get_message(url)

        if app_name == '':
            app_name = 'general'

        for acr, _ in settings.country_acr.items():
            unpack = resp.json()['data'][acr]

            print(m_name, unpack)

            if unpack:
                for index in xrange(len(unpack['data'])):
                    data = unpack['data'][index]
                    tmp = current_timestamp

                    if unpack.get('categories') is None:
                        message = '{0}.{1}.{2}.{3}'.format(settings.prefix, acr, m_name,
                                                           data['name'].encode('ascii', 'ignore'))
                        data = data['data']

                    elif isinstance(unpack['categories'][index], (int, float)):
                        tmp = unpack['categories'][index] / 1000 + settings.TIME_SHIFT
                        message = '{0}.{1}.{2}.{3}'.format(settings.prefix, acr, m_name, app_name)

                    else:
                        message = '{0}.{1}.{2}.{3}.{4}'.format(settings.prefix, acr, m_name, app_name, unpack['categories'][index])

                    print(message, data, tmp)

                    if data:
                        graphitesend.send(
                           metric=message,
                           value=data,
                           timestamp=tmp,
                        )

        execution += 1

print(execution)
