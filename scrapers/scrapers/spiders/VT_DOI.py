from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.spider import Spider, BaseSpider
from scrapy.http import Request

from scrapers.items import FileItem

import re
import urlparse


DOMAIN = 'dfr.vermont.gov'
URL = 'http://%s' % DOMAIN
state = 'VT'


class VT_DOI_Spider(CrawlSpider):

    name = 'vtdoi'
    allowed_domains = [DOMAIN]

    url = 'http://www.dfr.vermont.gov/view/regbul?tid=3&field_rb_type_value=Order'
    start_urls = [url + '&order=field_rb_date&sort=desc']

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

        item = FileItem(source='', name='', state='', year='',
                        grouped=[], gid='', checksum='', raw_text='')

        grouped = []

        for i in range(len(files)):
            url = files[i].xpath('@href').extract()[0]
            # reconstruct the absolute path to the file
            url = urlparse.urljoin(response.url, url.strip()).encode('ascii','ignore')

            grouped.append(url)

        for i in range(len(files)):
            url = files[i].xpath('@href').extract()[0]
            # reconstruct the absolute path to the file
            url = urlparse.urljoin(response.url, url.strip()).encode('ascii','ignore')
            
            name = title + " - " + str(i + 1)
            name = re.sub('[\\\/]',' ', name)

            item['source'] = url.encode('ascii','ignore')
            item['name'] = name
            item['state'] = state
            item['year'] = year
            item['grouped'] = grouped

            yield item
