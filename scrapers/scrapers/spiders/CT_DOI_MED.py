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


DOMAIN = 'ct.gov'
URL = 'http://%s' % DOMAIN
state = 'CT'


urls = ['http://www.ct.gov/cid/cwp/view.asp?q=289000',
        'http://www.ct.gov/cid/cwp/view.asp?a=1260&Q=471978',
        'http://www.ct.gov/cid/cwp/view.asp?a=1260&Q=453912']


class CT_DOI_Medicare_Spider(CrawlSpider):

    name = 'ctdoimed'
    allowed_domains = [DOMAIN]

    start_urls = urls

    def parse(self, response):

        sel = Selector(response)

        year = ''

        rowSelector = '//div//table//tbody//tr'
        rows = sel.xpath(rowSelector)
        for r in range(len(rows)):
            # 1. Check if the current row is a header row with the year on it
            # 2. If not, grab the link from the row and the text

            header = rows[r].xpath('th/text()')
            if header:
                year = header[0].extract()
                y = re.compile('\d\d\d\d')
                year = y.findall(year)
                if not year:
                    year = ['2014']
                year = year[0].encode('ascii', 'ignore').strip()
            else:

                links = rows[r].xpath('td//a[(contains(@href,"lib/cid"))]')
                group = default(FILEGROUP)

                for l in links:
                    text = l.xpath('text()').extract()
                    name = ''
                    if text:
                        item = default(FILEITEM)
                        url = l.xpath('@href').extract()[0]
                        url = urlparse.urljoin(
                            response.url, url.strip()).encode('ascii', 'ignore')

                        name = text[0].encode('ascii', 'ignore')
                        name = re.sub('[\\\?\*\"\.><\|\r\n]', '', name)
                        name = re.sub('[:\/]', '-', name)

                        item['source'] = url
                        item['name'] = name
                        item['state'] = state
                        item['year'] = year

                        group['items'].append(item)

                logging.info(group)
                yield group
