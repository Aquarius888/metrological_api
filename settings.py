# Current version of link to Metrological API
url_api = 'https://api.metrological.com/api/clientCountry'
# url_api = 'http://api-metrological/api/clientCountry'

# Current token (was taken form dashboard https://sso.metrological.com/#/login)
token = '0c17b77af4c2a23165901a5110b1cd6989f7169a6155565bd9ecad53b8df06a7'

# Proxy
# It must be an empty dictionary in case the script is run on host with direct connection or L7 routing to API server
proxy = {"https": "socks5://127.0.0.1:8888"}
# proxy = {}

# List of api type
app_type = ('widget', 'widgets', 'applications')

timespan = ('last60mins', 'lastweek')
timespan_options = '%7B%7D'  # {}
template_type = 'line'  # may be 'pie'

# dict of country acronyms and its IDs
# country_acr = {'nl': 1, 'de': 2, 'ch': 3, 'ie': 4, 'pl':5, 'hu': 6, 'cz': 13}
country_acr = {'nl': 1}

# settings for carbon server connectivity
# CARBON_SERVER = '172.27.66.160'
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
CARBON_PREFIX = ''
CARBON_SUFFIX = ''
CARBON_SYSTEM = ''

# To compensate time shift between response from metrologic (UTC) and local server time (UTC+1(winter),+2(summer))
TIME_SHIFT = 7200

# Level of logging (DEBUG, INFO, WARNING...)
loglevel = 'INFO'


# graphite format
prefix = 'app.metrological'

