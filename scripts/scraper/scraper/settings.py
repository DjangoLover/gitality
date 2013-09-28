import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

SCRAPY_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

BOT_NAME = 'scraper'

LOG_ENABLED = True
LOG_FILE = "/tmp/scraper.log"
LOG_LEVEL = 'INFO'

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

USER_AGENT = 'Gitality team.'
DOWNLOAD_DELAY = 1

FEED_FORMAT = 'json'

FEED_URI = os.path.join(SCRAPY_ROOT, "scraper/feeds/djangodash.json")
