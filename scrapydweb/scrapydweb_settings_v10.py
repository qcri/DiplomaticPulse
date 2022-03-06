# coding: utf-8
import os

SCRAPYDWEB_BIND = '0.0.0.0'
# Accept connections on the specified port, the default is 5000.
SCRAPYDWEB_PORT = 5000

# The default is False, set it to True to enable basic auth for the web UI.
ENABLE_AUTH = True
# In order to enable basic auth, both USERNAME and PASSWORD should be non-empty strings.
# These are provided in .env file
USERNAME = os.getenv('SCRAPY_WEB_USERNAME')
PASSWORD = os.getenv('SCRAPY_WEB_PASSWORD')

SCRAPYD_SERVERS = [
    os.getenv('SCRAPYD_SERVERS')
]

ENABLE_LOGPARSER = os.getenv("ENABLE_LOGPARSER", 'False').lower() in ('true', '1', 't')
LOCAL_SCRAPYD_LOGS_DIR = os.getenv('LOCAL_SCRAPYD_LOGS_DIR')

ENABLE_HTTPS = False
# e.g. '/home/username/cert.pem'
CERTIFICATE_FILEPATH = ''
# e.g. '/home/username/cert.key'
PRIVATEKEY_FILEPATH = ''
SCRAPY_PROJECTS_DIR = ''
SCRAPYD_LOG_EXTENSIONS = ['.log', '.log.gz', '.txt']

BACKUP_STATS_JSON_FILE = True

############################## Timer Tasks ####################################
# Run ScrapydWeb with argument '-sw' or '--switch_scheduler_state', or click the ENABLED|DISABLED button
# on the Timer Tasks page to turn on/off the scheduler for the timer tasks and the snapshot mechanism below.
JOBS_SNAPSHOT_INTERVAL = 300

############################## Run Spider #####################################
# The default is False, set it to True to automatically
# expand the 'dp_settings & arguments' section in the Run Spider page.
SCHEDULE_EXPAND_SETTINGS_ARGUMENTS = False

# The default is 'Mozilla/5.0', set it a non-empty string to customize the default value of `custom`
# in the drop-down list of `USER_AGENT`.
SCHEDULE_CUSTOM_USER_AGENT = 'Mozilla/5.0'

# The default is None, set it to any value of ['custom', 'Chrome', 'iPhone', 'iPad', 'Android']
# to customize the default value of `USER_AGENT`.
SCHEDULE_USER_AGENT = None

# The default is None, set it to True or False to customize the default value of `ROBOTSTXT_OBEY`.
SCHEDULE_ROBOTSTXT_OBEY = None

# The default is None, set it to True or False to customize the default value of `COOKIES_ENABLED`.
SCHEDULE_COOKIES_ENABLED = None

# The default is None, set it to a non-negative integer to customize the default value of `CONCURRENT_REQUESTS`.
SCHEDULE_CONCURRENT_REQUESTS = None

# The default is None, set it to a non-negative number to customize the default value of `DOWNLOAD_DELAY`.
SCHEDULE_DOWNLOAD_DELAY = None

# The default is "-d setting=CLOSESPIDER_TIMEOUT=60\r\n-d setting=CLOSESPIDER_PAGECOUNT=10\r\n-d arg1=val1",
# set it to '' or any non-empty string to customize the default value of `additional`.
# Use '\r\n' as the line separator.
SCHEDULE_ADDITIONAL = "-d setting=CLOSESPIDER_TIMEOUT=60\r\n-d setting=CLOSESPIDER_PAGECOUNT=10\r\n-d arg1=val1"


############################## Page Display ###################################
# The default is True, set it to False to hide the items page, as well as
# the items column in the Jobs page.
SHOW_SCRAPYD_ITEMS = True

# The default is True, set it to False to hide the Job column in the Jobs page with non-database view.
SHOW_JOBS_JOB_COLUMN = True

# The default is 0, which means unlimited, set it to a positive integer so that
# only the latest N finished jobs would be shown in the Jobs page with non-database view.
JOBS_FINISHED_JOBS_LIMIT = 0

# If your browser stays on the Jobs page, it would be reloaded automatically every N seconds.
# The default is 300, set it to 0 to disable auto-reloading.
JOBS_RELOAD_INTERVAL = 300

# The load status of the current Scrapyd server is checked every N seconds,
# which is displayed in the top right corner of the page.
# The default is 10, set it to 0 to disable auto-refreshing.
DAEMONSTATUS_REFRESH_INTERVAL = 10

# See step 1~7 above, e.g. 'xoxp-123-456-789-abcde'
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', '')
# The default channel to use when sending text via slack, e.g. 'general'
SLACK_CHANNEL = 'general'

########## telegram ##########
# How to create a telegram bot:

# See step 1~4 above, e.g. '123:abcde'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
# See step 5~6 above, e.g. 123456789
TELEGRAM_CHAT_ID = int(os.environ.get('TELEGRAM_CHAT_ID', 0))

############################## Monitor & Alert ################################
ENABLE_MONITOR = True

########## poll interval ##########
POLL_ROUND_INTERVAL = 300
# Sleep N seconds between each request to the Scrapyd server while polling, the default is 10.
POLL_REQUEST_INTERVAL = 10
ENABLE_SLACK_ALERT = False
ENABLE_TELEGRAM_ALERT = False
ENABLE_EMAIL_ALERT = True

########## alert working time ##########
# Monday is 1 and Sunday is 7.
# e.g, [1, 2, 3, 4, 5, 6, 7]
ALERT_WORKING_DAYS = [1, 2, 3, 4, 5, 6, 7]

# From 0 to 23.
# e.g. [9] + list(range(15, 18)) >>> [9, 15, 16, 17], or range(24) for 24 hours
ALERT_WORKING_HOURS = list(range(9, 17))

########## basic triggers ##########
# Trigger alert every N seconds for each running job.
# The default is 0, set it to a positive integer to enable this trigger.
ON_JOB_RUNNING_INTERVAL = 60

# Trigger alert when a job is finished.
# The default is False, set it to True to enable this trigger.
ON_JOB_FINISHED = False

LOG_CRITICAL_THRESHOLD = 1
LOG_CRITICAL_TRIGGER_STOP = False
LOG_CRITICAL_TRIGGER_FORCESTOP = False

LOG_ERROR_THRESHOLD = 3
LOG_ERROR_TRIGGER_STOP = False
LOG_ERROR_TRIGGER_FORCESTOP = False

LOG_WARNING_THRESHOLD = 0
LOG_WARNING_TRIGGER_STOP = False
LOG_WARNING_TRIGGER_FORCESTOP = False

LOG_REDIRECT_THRESHOLD = 0
LOG_REDIRECT_TRIGGER_STOP = False
LOG_REDIRECT_TRIGGER_FORCESTOP = False

LOG_RETRY_THRESHOLD = 10
LOG_RETRY_TRIGGER_STOP = False
LOG_RETRY_TRIGGER_FORCESTOP = False

LOG_IGNORE_THRESHOLD = 0
LOG_IGNORE_TRIGGER_STOP = False
LOG_IGNORE_TRIGGER_FORCESTOP = False


############################## System #########################################
# The default is False, set it to True to enable debug mode and the interactive debugger
# would be shown in the browser instead of the "500 Internal Server Error" page.
# Note that use_reloader is set to False in run.py
DEBUG = False

# The default is False, set it to True to change the logging level from INFO to DEBUG
# for getting more information about how ScrapydWeb works, especially while debugging.
VERBOSE = False

# The default is '', which means saving all program data in the Python directory.
# e.g. 'C:/Users/username/scrapydweb_data' or '/home/username/scrapydweb_data'
DATA_PATH = os.environ.get('DATA_PATH', '')

DATABASE_URL = os.environ.get('DATABASE_URL', '')