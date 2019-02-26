"""
Metrological API metrics ingestion (daily metrics)
Graphite delivery

## Deploy notes

Before deploy, navigate to: http://airflow-vie.horizon.tv/admin/variable/
and make sure following variables are set:

 * metrological_token: token for Metrological API (may be taken from keeweb)
 * metrological_url_api: actual url of API or responsible alias
 * metrological_thread: amount of request's threads (must be equal 'N', str #194)

 If the DAG is going to be executed on Airflow under python3, change all xrange to range
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

import time
from datetime import datetime, timedelta

from utils import metrogenerator
from utils.graphite import Graphite


token = str(Variable.get('metrological_token'))
url_api = str(Variable.get('metrological_url_api'))
thread = int(Variable.get('metrological_thread'))

GLOBAL_GRAPHITE_PREFIX = 'app.metrological'
# To compensate time shift between response from metrologic (UTC) and local server time (UTC+1(winter),+2(summer))
TIME_SHIFT = 7200

headers = {'X-Api-Token': token}
country_acr = {'nl': 1, 'de': 2, 'ch': 3, 'ie': 4, 'pl': 5, 'hu': 6, 'cz': 13}
api_type = ('widget', 'widgets', 'applications')
proxy = {}
timespan = ('last60mins', 'lastweek')
timespan_options = '%7B%7D'
template_type = 'line'
current_timestamp = int(time.time())


m = metrogenerator.Metro(url_api, proxy, headers)


def collect_urls(**context):
    """
    Make requests to Metrological API
    :param context: airflow syntax
    :return: list of urls for requesting
    """

    api_type = context['params']['api_type']
    timespan = context['params']['timespan']
    country_acr = context['params']['country_acr']
    timespan_options = context['params']['timespan_options']
    template_type = context['params']['template_type']

    app_id_json = m.get_allowed(api_type[1], 'allowedApps')

    list_apps_id = [app_id_json['apps'][n]['id'] for n in xrange(len(app_id_json['apps']))
                    if 'test' not in app_id_json['apps'][n]['id'].lower()
                    and 'example' not in app_id_json['apps'][n]['id'].lower()]

    widgets_json = m.get_allowed(api_type[1], 'widgets-i-can-create')
    daily_metrics, app_list_req = m.get_metric_list(widgets_json, timespan[0])

    non_req = list(set(daily_metrics) - set(app_list_req))

    urls = [m.get_url(api_type[0], metric_name, m.get_country_str(country_acr),
                      timespan[0], timespan_options, template_type, app_id='')
            for metric_name in non_req]

    urls_app = [m.get_url(api_type[0], metric_name, m.get_country_str(country_acr),
                          timespan[0], timespan_options, template_type, app_id)
                for metric_name in app_list_req for app_id in list_apps_id]
    urls.extend(urls_app)
    return urls


def break_list(**context):
    """
    Break list of urls on list of amount lists
    :param context: airflow syntax
    :return: list of lists
    """
    thread = context['params']['thread']
    urls = context['task_instance'].xcom_pull(task_ids='collect_urls')
    broken_list = [urls[i*len(urls)//thread:(i+1)*len(urls)//thread] for i in xrange((len(urls))//thread)]
    return broken_list


def get_n_publish(**context):
    """Request, format and publish metrics
    :param context: airflow syntax
    :return: amount of successful requests
    """
    test_mode = bool(context['test_mode'])
    carbon_host = str(Variable.get('carbon_host'))
    carbon_port = int(Variable.get('carbon_port'))
    country_acr = context['params']['country_acr']
    prefix = context['params']['prefix']
    time_shift = context['params']['time_shift']
    i = context['params']['i']
    urls = context['task_instance'].xcom_pull(task_ids='break_list')
    pointer = 0
    for url in urls[i]:
        resp = m.get_response(url)
        if resp.status_code == 200:
            m_name, app_name = m.get_message(url)

            if app_name == '':
                app_name = 'general'

            for acr, _ in country_acr.items():
                unpack = resp.json()['data'][acr]

                if unpack:
                    for index in xrange(len(unpack['data'])):
                        data = unpack['data'][index]
                        tmp = current_timestamp

                        if unpack.get('categories') is None:
                            message = '{0}.{1}.{2}.{3}'.format(prefix, acr, m_name,
                                                               str(data['name'].encode('ascii', 'ignore')))
                            data = data['data']

                        elif isinstance(unpack['categories'][index], (int, float)):
                            tmp = unpack['categories'][index] / 1000 + time_shift
                            message = '{0}.{1}.{2}.{3}'.format(prefix, acr, m_name, app_name)

                        else:
                            message = '{0}.{1}.{2}.{3}'.format(prefix, acr, m_name,
                                                               unpack['categories'][index])

                        metrics = (message, data, tmp)
                        pointer += 1

                        g = Graphite(carbon_host, carbon_port, test_mode)
                        g.send(metrics)
    return pointer


##################################################################################################################
# DAG
##################################################################################################################
dag = DAG(
    dag_id='metrological_metrics_daily',
    schedule_interval=timedelta(minutes=60),
    dagrun_timeout=timedelta(minutes=5),
    max_active_runs=1,
    catchup=False,
    default_args={
        'start_date': datetime(2016, 11, 22),
        'depends_on_past': False,
    },
)

task_collect_urls = PythonOperator(
    task_id='collect_urls',
    python_callable=collect_urls,
    dag=dag,
    provide_context=True,
    params={
            'api_type': api_type,
            'timespan': timespan,
            'country_acr': country_acr,
            'timespan_options': timespan_options,
            'template_type': template_type,
    },
)

task_break_list = PythonOperator(
    task_id='break_list',
    python_callable=break_list,
    dag=dag,    
    provide_context=True,
    params={
            'thread': thread,
    },
)


task_collect_urls >> task_break_list

# xrange(N), N must be equal thread
for i in xrange(5):
    task_get_n_publish = PythonOperator(
        task_id='get_n_publish' + str(i),
        python_callable=get_n_publish,
        provide_context=True,
        dag=dag,
        task_concurrency=10,
        params={
            'country_acr': country_acr,
            'prefix': GLOBAL_GRAPHITE_PREFIX,
            'time_shift': TIME_SHIFT,
            'i': i,
        },
    )
    task_break_list >> task_get_n_publish

# doctest
if __name__ == '__main__':
    import doctest

    doctest.testmod()
