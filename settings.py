# Current version of link to Metrological API
url_api = 'https://api.metrological.com/api/clientCountry'

# Current token (was taken form dashboard https://sso.metrological.com/#/login)
token = '0c17b77af4c2a23165901a5110b1cd6989f7169a6155565bd9ecad53b8df06a7'


# Dictionary of metrics and its properties
metric = {'most_apps_openend_on_channel': ['widget', 'AppsOpenedOnChannel'],
          'engagement_rate': ['widget', 'EngagementRateLastWeek', 'timestamp_lastweek'],
          'videos_started': ['widget', 'VideoStarted'],
          'video_duration': ['widget', 'VideoDuration'],
          'top_app_video_playback': ['widget', 'TopAppsVideoPlayback'],
          'household_engagement': ['widget', 'HouseholdEngagement', 'timestamp_lastweek'],
          'top_app_video_duration': ['widget', 'TopAppVideoDuration'],
          'total_households': ['widget', 'TotalHouseholds'],
          'unique_households': ['widget', 'UniqueHouseholds'],
          'average_app_usage': ['widget', 'AverageAppLaunches'],
          'top_app_view': ['widget', 'MostPagesViewedInApp'],
          'app_launches_per_customer': ['widget', 'AppLaunchPerCustomerLastMonth', 'timestamp_lastweek'],
          'visits_per_customer': ['widget', 'VisitsPerCustomer', 'timestamp_lastweek'],
          'app_store_visits_per_customer': ['widget', 'AppStoreVisitPerCustomer'],
          'most_favorited_app': ['widget', 'MostFavoritedApps'],
          'avg_session_length': ['widget', 'AverageSessionLength'],
          'app_unique_user': ['widget', 'UniqueUser7Days'],
          'apps_opened_per_category': ['widget', 'OpenedPerCategoryLast30Days'],
          'apps_opened': ['widget', 'OpenedYesterday'],
          'active_households': ['widget', 'ActiveHouseholdsYesterday'],
          'data_engagement_waterfall': ['widget', 'WaterfallLast7Days', 'timestamp_lastweek'],
          'top_apps': ['widget', 'TopApps'],
          # following metrics require list of application's ids
          'app_time_spend': ['widget', 'AvgTimeInApp', 'list apps id is required'],
          'app_amount_opened': ['widget', 'TotalAppStarts', 'list apps id is required'],
          'app_video_duration': ['widget', 'AppVideoDuration', 'list apps id is required']}

additional_metrics = {'allowedApps': ['widgets', 'GetAllowedApps'],
                      'chanelHash': ['socket', 'RealTimeAppsClosed'],  # realtime, How to use it with our schedule?
                      'performance': ['applications', 'Avg_Load_Time']}  # is it necessary?

# Id of application, in future it may be come list of ids
app_id = 'com.metrological.app.NetflixHorizon'

timespan = ['today', 'last7days', 'last24hours', 'lastweek', 'lastmonth', 'yesterday', 'last30days']
timespan_options = '%7B%7D' #{}
template_type = 'line' # may be 'pie'

# dict of country acronyms and its IDs
country_acr = {'nl': 1, 'de': 2, 'ch': 3, 'ie': 4, 'pl':5, 'hu': 6, 'cz': 13}

# settings for carbon server connectivity
# CARBON_SERVER = '172.27.66.160'
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
CARBON_PREFIX = ''
CARBON_SUFFIX = ''
CARBON_SYSTEM = ''

# To compensate time shift between response from metrologic (UTC) and local server time (UTC+1(winter),+2(summer))
TIME_SHIFT = 7200
