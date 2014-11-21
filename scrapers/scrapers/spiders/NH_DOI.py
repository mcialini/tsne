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


DOMAIN = 'nh.gov'
URL = 'http://%s' % DOMAIN
state = 'NH'
logging.info('\n-----------\nNHDOI\n------------')


class NH_DOI_Spider(CrawlSpider):

    name = 'nhdoi'
    allowed_domains = [DOMAIN]

    url = 'http://www.nh.gov/insurance/legal/enforcement/index.htm'
    start_urls = [url]

    rules = (
        # Follow all pages that have the tables we're interested in
        Rule(SgmlLinkExtractor(allow=('\d\d\d\d'), unique=True),
             callback='parse_items'),
        # Pass the pages for each individual enforcement action to the parse_items function
        # so that the document can be downloaded
    )

    def parse_items(self, response):

        sel = Selector(response)

        # Find the date of the order
        dateSelector = '//td[@class="title"]/text()'
        date = " ".join(sel.xpath(dateSelector).extract())
        y = re.compile('\d\d\d\d')
        year = y.findall(date)[0].encode('ascii', 'ignore').strip()

        # Find the file we want to download
        rowSelector = '//table[@id="blue_table"]//tr'
        rows = sel.xpath(rowSelector)

        # 1. Single link with company name as a/text
        # 2. Line of text with company name, and one or more links to documentsd
        # 3. Multiple links, top one having the company name
        if year == '2014':
            for r in rows:
                group = default(FILEGROUP)

                col = r.xpath('td')
                # the column we're interested in is not empty, so let's scrape
                # it
                if col:

                    titleSelector1 = 'div//p/text()'
                    titleSelector2 = 'div//text()'
                    titleSelector3 = 'div//span/text()'
                    titleSelector4 = 'p//span/text()'
                    titleSelector5 = 'p/text()'
                    titleSelector6 = 'span/text()'
                    titleSelector7 = 'text()'

                    titles1 = col[0].xpath(titleSelector1)
                    titles2 = col[0].xpath(titleSelector2)
                    titles3 = col[0].xpath(titleSelector3)
                    titles4 = col[0].xpath(titleSelector4)
                    titles5 = col[0].xpath(titleSelector5)
                    titles6 = col[0].xpath(titleSelector6)
                    titles7 = col[0].xpath(titleSelector7)

                    compname = ''

                    if titles1:
                        compname = re.sub(' +', ' ', titles1[0].extract()).strip().encode(
                            'ascii', 'ignore')
                        compname = re.sub('[\\\?\*\"\.><\|\r\n]', '', compname)
                        ##f.write(titleSelector1 + '\n')
                    elif titles2:
                        compname = re.sub(' +', ' ', titles2[0].extract()).strip().encode(
                            'ascii', 'ignore')
                        compname = re.sub('[\\\?\*\"\.><\|\r\n]', '', compname)
                        ##f.write(titleSelector2 + '\n')
                    elif titles3:
                        compname = re.sub(
                            ' +', ' ', titles3[0].extract()).strip().encode('ascii', 'ignore')
                        compname = re.sub('[\\\?\*\"\.><\|\r\n]', '', compname)
                        ##f.write(titleSelector3 + '\n')
                    elif titles4:
                        compname = re.sub(
                            ' +', ' ', titles4[0].extract()).strip().encode('ascii', 'ignore')
                        compname = re.sub('[\\\?\*\"\.><\|\r\n]', '', compname)
                        ##f.write(titleSelector4 + '\n')
                    elif titles5:
                        compname = re.sub(' +', ' ', titles5[0].extract()).strip().encode(
                            'ascii', 'ignore')
                        compname = re.sub('[\\\?\*\"\.><\|\r\n]', '', compname)
                        ##f.write(titleSelector5 + '\n')
                    elif titles6:
                        compname = re.sub(
                            ' +', ' ', titles6[0].extract()).strip().encode('ascii', 'ignore')
                        compname = re.sub('[\\\?\*\"\.><\|\r\n]', '', compname)
                        ##f.write(titleSelector6 + '\n')
                    elif titles7:
                        compname = re.sub(
                            ' +', ' ', titles7[0].extract()).strip().encode('ascii', 'ignore')
                        compname = re.sub('[\\\?\*\"\.><\|\r\n]', '', compname)
                        ##f.write(titleSelector7 + '\n')

                    # If no title was found, then just use the first link as the
                    # company name
                    if compname == '':
                        titleCatch1 = 'a/text()'
                        titleCatch2 = 'div//a/text()'
                        title1 = col[0].xpath(titleCatch1)
                        title2 = col[0].xpath(titleCatch2)
                        if title1:
                            compname = re.sub(' +', ' ', title1[0].extract()).strip().encode(
                                'ascii', 'ignore')
                            compname = re.sub(
                                '[\\\?\*\"\.><\|\r\n]', '', compname)
                        elif title2:
                            compname = re.sub(' +', ' ', title2[0].extract()).strip().encode(
                                'ascii', 'ignore')
                            compname = re.sub(
                                '[\\\?\*\"\.><\|\r\n]', '', compname)
                    #f.write(compname + '\n')

                    name = ''
                    url = ''

                    links1 = col[0].xpath('a')
                    links2 = col[0].xpath('div//a')
                    links3 = col[0].xpath('p//a')

                    if links1:
                        for l in links1:
                            item = default(FILEITEM)
                            name = l.xpath('text()').extract()[0]
                            name = re.sub(' +', ' ', name).strip().encode(
                                'ascii', 'ignore')
                            name = re.sub('[\\\?\*\"\.><\|\r\n]', '', name)
                            item['name'] = compname + ' ' + name

                            url = l.xpath('@href').extract()[0]
                            url = urlparse.urljoin(
                                response.url, url.strip()).encode('ascii', 'ignore')

                            item['source'] = url
                            item['name'] = name
                            item['state'] = state
                            item['year'] = year
                            group['items'].append(item)

                    elif links2:
                        for l in links2:
                            item = default(FILEITEM)
                            name = l.xpath('text()').extract()[0]
                            name = re.sub(' +', ' ', name).strip().encode(
                                'ascii', 'ignore')
                            name = re.sub('[\\\?\*\"\.><\|\r\n]', '', name)
                            item['name'] = compname + ' ' + name

                            url = l.xpath('@href').extract()[0]
                            url = urlparse.urljoin(
                                response.url, url.strip()).encode('ascii', 'ignore')

                            item['source'] = url
                            item['name'] = name
                            item['state'] = state
                            item['year'] = year
                            group['items'].append(item)

                    elif links3:
                        for l in links3:
                            item = default(FILEITEM)
                            name = l.xpath('text()').extract()[0]
                            name = re.sub(' +', ' ', name).strip().encode(
                                'ascii', 'ignore')
                            name = re.sub('[\\\?\*\"\.><\|\r\n]', '', name)
                            item['name'] = re.sub(
                                '[\\\?\*\"\.><\|\r\n]', '', name)
                            item['name'] = compname + ' ' + name

                            url = l.xpath('@href').extract()[0]
                            url = urlparse.urljoin(
                                response.url, url.strip()).encode('ascii', 'ignore')

                            item['source'] = url
                            item['name'] = name
                            item['state'] = state
                            item['year'] = year
                            group['items'].append(item)

                    logging.info('SCRAPED > ' + str(len(group['items'])))
                    yield group
