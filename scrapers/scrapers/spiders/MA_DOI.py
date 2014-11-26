from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.spider import Spider, BaseSpider
from scrapy.http import Request

from scrapers.items import default, FILEGROUP, FILEITEM
import scrapers.config as config
import logging

import re


DOMAIN = 'mass.gov'
URL = 'http://%s' % DOMAIN
state = 'MA'
logging.info('\n-----------\nMADOI\n------------')


class MA_DOI_Spider(CrawlSpider):

    name = 'madoi'
    allowed_domains = [DOMAIN]

    start_urls = [
        'http://www.mass.gov/ocabr/insurance/providers-and-producers/insurance-producers/enforcement/doi-administrative-actions']

    rules = (
        # Follow the links for each year of actions
        Rule(
            LxmlLinkExtractor(
                allow=(
                    "\d\d\d\d-doi-administrative-actions/",
                    "\d\d\d\d-doi-admin-actions/",
                )
            ),
        ),
        # Do simple parse of pdf links
        Rule(
            SgmlLinkExtractor(
                allow=(
                    "\d\d\d\d-doi-administrative-actions/",
                    "\d\d\d\d-doi-admin-actions/",
                )
            ),    
        ),
        # Parse HTML documents individually and create items for each row of the table
    )

    def parse_items(self, response):
        sel = Selector(response)

        getpdfs = '//a[(contains(@href, "enforcementactions.pdf") or contains(@href, "admin")) and contains(@class, "titlelink")]'

        links = sel.xpath(getpdfs)

        for link in links:
            item = default(FILEITEM)
            group = default(FILEGROUP)

            url = URL + link.xpath('@href').extract()[0]
            name = link.xpath('text()').extract()

            y = re.compile('\d\d\d\d')
            year = y.findall(name[0])[0].encode('ascii', 'ignore').strip()

            name = re.search(': (.*)', name[0].encode('ascii', 'ignore'))
            name = name.group(1)

            item['source'] = url
            item['name'] = name
            item['state'] = state
            item['year'] = year
            group['items'].append(item)

            logging.info('SCRAPED > ' + str(len(group['items'])))
            yield group
