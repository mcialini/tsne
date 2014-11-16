from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.spider import Spider, BaseSpider
from scrapy.http import Request

from scrapers.items import default, FILEITEM, FILEGROUP
import scrapers.config as config
import logging

import re
import urlparse


DOMAIN = 'dbr.state.ri.us'
URL = 'http://%s' % DOMAIN
state = 'RI'


class RI_DOI_Spider(CrawlSpider):

    name = 'ridoi'
    allowed_domains = [DOMAIN]

    start_urls = [
        'http://www.dbr.state.ri.us/decisions/decisions_insurance.php']

    def parse(self, response):

        sel = Selector(response)

        rowSelector = '//table[@class="datatable"]//tr'
        rows = sel.xpath(rowSelector)


        for r in rows:
            col = r.xpath('td')
            if col:
                item = default(FILEITEM)
                group = default(FILEGROUP)

                name = col[0].xpath('text()').extract()[0]
                url = col[1].xpath('a//@href').extract()[0]
                year = col[2].xpath('text()').extract()[0]

                name = re.sub(' +', ' ', name).strip().encode(
                    'ascii', 'ignore')
                name = re.sub('[\\\?\*\"\.><\|\r\n]', '', name)
                name = re.sub('[\/:]', '-', name)
                name = re.sub('[;]', ',', name)

                url = urlparse.urljoin(response.url, url.strip())
                y = re.compile('\d\d\d\d')
                year = y.findall(year)[0].encode('ascii', 'ignore')

                if year == '1007':
                    year = '2007'

                item['source'] = url.encode('ascii', 'ignore')
                item['name'] = name
                item['state'] = state
                item['year'] = year
                group['items'].append(item)

                logging.info('SCRAPING > ' + str(len(group['items'])))
                yield group
