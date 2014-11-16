# Scrapy settings for scrapers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
BOT_NAME = 'scrapers'

SPIDER_MODULES = ['scrapers.spiders']
NEWSPIDER_MODULE = 'scrapers.spiders'


ITEM_PIPELINES = {	
	'scrapers.verify.VerificationPipeline': 0,
	'scrapers.download.DownloadingPipeline' : 1,
	'scrapers.extract.ExtractionPipeline': 2,
	'scrapers.polish.PolishingPipeline': 3,
	'scrapers.insert.InsertionPipeline': 4
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapers (+http://www.yourdomain.com)'
