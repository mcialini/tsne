from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.spider import Spider, BaseSpider
from scrapy.http import Request

from scrapers.items import FileItem

import re


DOMAIN = 'mass.gov'
URL = 'http://%s' % DOMAIN
state = 'MA'


class MA_DOB_Spider(CrawlSpider):

    name = 'madob'
    allowed_domains = [DOMAIN]

    start_urls = [
        'http://www.mass.gov/ocabr/banking-and-finance/laws-and-regulations/enforcement-actions']

    rules = (
        Rule(SgmlLinkExtractor(allow=("\d\d\d\d-dob-enforcement-actions/", "\d\d\d\d-enforcement-actions/"), unique=True), callback='parse_items', ),)

    def parse_items(self, response):
        sel = Selector(response)

        titleSelector = '//head//title'
        linkSelector = '//div[contains(@class,"col") and contains(@class,"introduction")]//ul//li//h2//a[@class="titlelink"]'

        title = sel.xpath(titleSelector)
        links = sel.xpath(linkSelector)

        year = title.xpath('text()').extract()[0].encode(
            'ascii', 'ignore').strip().replace(" (Continued)", "").replace("DOB ", "")

        item = FileItem(source='', name='', state='', year='',
                        grouped=[], gid='', checksum='', raw_text='')

        for link in links:
            url = link.xpath('@href').extract()[0].encode('ascii','ignore')
            url = URL + url
            name = link.xpath('text()').extract()[0].encode('ascii', 'ignore')

            name = re.sub('[\\\/\?\*\"\.><\|]', '', name).replace(':', '-')

            item['source'] = url.encode('ascii', 'ignore')
            item['name'] = name
            item['state'] = state
            item['year'] = year

            yield item
