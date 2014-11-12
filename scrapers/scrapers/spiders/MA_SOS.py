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


DOMAIN = 'sec.state.ma.us'
URL = 'http://%s' % DOMAIN
state = 'MA'


class MA_SOS_Spider(CrawlSpider):

    name = 'masos'
    allowed_domains = [DOMAIN]

    start_urls = [
        'http://www.sec.state.ma.us/sct/archived/sct_archives_2012.htm',
        'http://www.sec.state.ma.us/sct/archived/sct_archives_2011.htm',
        'http://www.sec.state.ma.us/sct/archived/sct_archives_2010.htm',
        'http://www.sec.state.ma.us/sct/archived/sct_archives_2009.htm']

    # links of form sct/*/*idx.htm
    rulestr = "sct\/.*/.*idx\.htm"
    rules = (Rule(SgmlLinkExtractor(allow=(rulestr), unique=True, restrict_xpaths=(
        '//div[@id="outer"]//div[@id="wrapper"]//div[@id="content_third"]')), callback='parse_items', ),)

    def parse_items(self, response):

        sel = Selector(response)

        titleSelector = '//div[@id="outer"]//div[@id="wrapper"]//div[@id="content_third"]//h1'

        # this selector should grab the entire content_third div form each
        # individual actions page
        linkSelector = '//div[@id="outer"]//div[@id="wrapper"]//div[@id="content_third"]//p//a'

        title = sel.xpath(titleSelector)
        links = sel.xpath(linkSelector)

        action = title.xpath('text()').extract()

        action = ' '.join(action)
        action = re.sub(' +', ' ', action).rstrip().encode('ascii', 'ignore')
        action = re.sub('[\\\?\*\"\.><\|\r\n]', '', action)
        action = re.sub('[:\/]', '-', action)

        item = FileItem(source='', name='', state='', year='',
                        grouped=[], gid='', checksum='', raw_text='')

        for link in links:
            url = link.xpath('@href').extract()[0]

            # reconstruct the absolute path to the file
            url = urlparse.urljoin(response.url, url.strip())

            name = link.xpath('text()').extract()[0].encode('ascii', 'ignore')
            name = re.sub('[\\\?\*\"\.><\|\r\n]', '', name)
            name = re.sub('[:\/]', '-', name)

            name = action + ' - ' + name
            year = ''

            item['source'] = url.encode('ascii', 'ignore')
            item['name'] = name
            item['state'] = state
            item['year'] = year
            
            yield item
