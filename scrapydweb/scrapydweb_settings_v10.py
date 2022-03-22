# coding: utf-8
"""
How ScrapydWeb works:
GitHub: https://github.com/my8100/scrapydweb
DOCS: https://github.com/my8100/files/blob/master/scrapydweb/README.md
"""
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
    os.getenv('SCRAPYD_SERVERS'),
]

ENABLE_LOGPARSER = os.getenv("ENABLE_LOGPARSER", 'False').lower() in ('true', '1', 't')
LOCAL_SCRAPYD_LOGS_DIR = os.getenv('LOCAL_SCRAPYD_LOGS_DIR')

############################## ScrapydWeb #####################################
# The default is False, set it to True and add both CERTIFICATE_FILEPATH and PRIVATEKEY_FILEPATH
ENABLE_HTTPS = False

CERTIFICATE_FILEPATH = ''

PRIVATEKEY_FILEPATH = ''

############################## Scrapy #########################################
# ScrapydWeb is able to locate projects in the SCRAPY_PROJECTS_DIR,
SCRAPY_PROJECTS_DIR = ''

############################## Scrapyd ########################################
# ScrapydWeb would try every extension in sequence to locate the Scrapy logfile.
# The default is ['.log', '.log.gz', '.txt'].
SCRAPYD_LOG_EXTENSIONS = ['.log', '.log.gz', '.txt']

############################## LogParser ######################################
# Whether to backup the stats json files locally after you visit the Stats page of a job
# so that it is still accessible even if the original logfile has been deleted.
# The default is True, set it to False to disable this behaviour.
BACKUP_STATS_JSON_FILE = True

############################## Timer Tasks ####################################
# Run ScrapydWeb with argument '-sw' or '--switch_scheduler_state', or click the ENABLED|DISABLED button
# on the Timer Tasks page to turn on/off the scheduler for the timer tasks and the snapshot mechanism below.

# The default is 300, which means ScrapydWeb would automatically create a snapshot of the Jobs page
# and save the jobs info in the database in the background every 300 seconds.
# Note that this behaviour would be paused if the scheduler for timer tasks is disabled.
# Set it to 0 to disable this behaviour.
JOBS_SNAPSHOT_INTERVAL = 300

############################## Run Spider #####################################
# The default is False, set it to True to automatically
# expand the 'settings & arguments' section in the Run Spider page.
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
# The default is True, set it to False to hide the Items page, as well as
# the Items column in the Jobs page.
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

########## slack ##########
# How to create a slack app:
# See https://api.slack.com/apps for more info

# See step 1~7 above, e.g. 'xoxp-123-456-789-abcde'
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', '')
# The default channel to use when sending text via slack, e.g. 'general'
SLACK_CHANNEL = 'general'

########## telegram ##########
# How to create a telegram bot:
# See https://core.telegram.org/bots#6-botfather for more info

# See step 1~4 above, e.g. '123:abcde'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
# See step 5~6 above, e.g. 123456789
TELEGRAM_CHAT_ID = int(os.environ.get('TELEGRAM_CHAT_ID', 0))

########## email ##########
# The default subject to use when sending text via email.
EMAIL_SUBJECT = 'Email from #scrapydweb'

########## email sender & recipients ##########
# Leave this option as '' to default to the EMAIL_SENDER option below; Otherwise, set it up
# if your email service provider requires an username which is different from the EMAIL_SENDER option below to login.
# e.g. 'username'
EMAIL_USERNAME = 'dpulse@qcri.org'
# https://stackoverflow.com/a/26053352/10517783 Python smtplib proxy support

EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'x6@hdC=2')

EMAIL_SENDER = 'dpulse@qcri.org'
# e.g. ['username@gmail.com', ]
EMAIL_RECIPIENTS = ['test@test.com']#

########## email smtp settings ##########
# Check out this link if you are using ECS of Alibaba Cloud and your SMTP server provides TCP port 25 only:
# https://www.alibabacloud.com/help/doc-detail/56130.htm

SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_OVER_SSL = False
# The timeout in seconds for the connection attempt, the default is 30.
SMTP_CONNECTION_TIMEOUT = 30

############################## Monitor & Alert ################################
# The default is False, set it to True to launch the poll subprocess to monitor your crawling jobs.
ENABLE_MONITOR = True

########## poll interval ##########
# Tip: In order to be notified (and stop or forcestop a job when triggered) in time,
# you can reduce the value of POLL_ROUND_INTERVAL and POLL_REQUEST_INTERVAL,
# at the cost of burdening both CPU and bandwidth of your servers.

# Sleep N seconds before starting next round of poll, the default is 300.
POLL_ROUND_INTERVAL = 300
# Sleep N seconds between each request to the Scrapyd server while polling, the default is 10.
POLL_REQUEST_INTERVAL = 10

########## alert switcher ##########
# Tip: Set the SCRAPYDWEB_BIND option the in "QUICK SETUP" section to the actual IP of your host,
# then you can visit ScrapydWeb via the links attached in the alert.

# The default is False, set it to True to enable alert via Slack, Telegram, or Email.
# You have to set up your accounts in the "Send text" section above first.
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

########## advanced triggers ##########
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
DEBUG = False

VERBOSE = False

DATA_PATH = os.environ.get('DATA_PATH', '')

DATABASE_URL = os.environ.get('DATABASE_URL', '')