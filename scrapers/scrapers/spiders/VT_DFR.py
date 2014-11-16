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
import urlparse


DOMAIN = 'dfr.vermont.gov'
URL = 'http://%s' % DOMAIN
state = 'VT'


class VT_DFR_Spider(CrawlSpider):

    name = 'vtdfr'
    allowed_domains = [DOMAIN]

    url = 'http://www.dfr.vermont.gov/view/regbul?tid=3&field_rb_type_value=Market+Conduct'
    start_urls = [url]

    rules = (
        # Follow all pages that have the tables we're interested in
        Rule(SgmlLinkExtractor(allow=('&page='), unique=True), follow=True, ),
        # Pass the pages for each individual enforcement action to the parse_items function
        # so that the document can be downloaded
        Rule(SgmlLinkExtractor(allow=('reg-bul-ord'), unique=True),
             callback='parse_items', ),
    )

    def parse_items(self, response):

        sel = Selector(response)

        # Find the name of the order
        titleSelector = '//h1[@id="page-title"]/text()'
        title = sel.xpath(titleSelector).extract()[0].encode('ascii', 'ignore')

        # Find the date of the order
        dateSelector = '//span[@class="date-display-single"]/text()'
        date = sel.xpath(dateSelector).extract()[0]
        y = re.compile('\d\d\d\d')
        year = y.findall(date)[0].encode('ascii', 'ignore')

        # Find the file we want to download
        fileSelector = '//span[@class="file"]//a'
        files = sel.xpath(fileSelector)

        item = default(FILEITEM)
        group = default(FILEGROUP)

        for i in range(len(files)):
            url = files[i].xpath('@href').extract()[0]
            # reconstruct the absolute path to the file
            url = urlparse.urljoin(
                response.url, url.strip()).encode('ascii', 'ignore')

            name = files[i].xpath('text()').extract()[0].replace('.pdf', '')
            name = (re.sub('[\\\?\*\"\.><\|\r\n]', '', title).replace('/', ' ') + ' - ' + re.sub(
                '[\\\?\*\"\.><\|\r\n]', '', name)).replace(', ', ',')

            item['source'] = url
            item['name'] = name
            item['state'] = state
            item['year'] = year

            group['items'].append(item)
            item = default(FILEITEM)

        logging.info(group['items'][0]['name'])
        logging.info(len(group['items']))
        yield group
