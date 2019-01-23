url_api = 'https://api.metrological.com/api/clientCountry'
metric = {'app_time_spend': ['widget', 'AvgTimeSpend'],
          'app_unique_user': ['widget', 'UniqUser7Days'],
          'app_amount_opened': ['widget', 'OpenedLast7Days'],
          'performance': ['applications', 'Avg_Load_Time']}
token = '0c17b77af4c2a23165901a5110b1cd6989f7169a6155565bd9ecad53b8df06a7'
app_id = 'com.metrological.app.NetflixHorizon'
timespan = ['today', 'last7days']
timespan_options = '%7B%7D' #{}
template_type = 'line'

country_acr = ['nl', 'de', 'ch', 'ie']

# CARBON_SERVER = '172.27.66.160'
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
CARBON_PREFIX = ''
CARBON_SUFFIX = ''
CARBON_SYSTEM = ''
# To compensate time shift between response from
# metrologic (UTC) and local server time (UTC+1(winter),+2(summer))
TIME_SHIFT = 7200
