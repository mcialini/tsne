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


DOMAIN = 'maine.gov'
URL = 'http://%s' % DOMAIN
state = 'ME'


class ME_DOI_Spider(CrawlSpider):

    name = 'medoi'
    allowed_domains = [DOMAIN]

    start_urls = [
        'http://www.maine.gov/pfr/insurance/consent_agreements/date_list.htm']

    def parse(self, response):

        sel = Selector(response)

        titleSelector = '//head//title'
        linkSelector = '//a[contains(@href,"\d\d\d\d")]'

        linkSelector = '//body//td[@id="awt-middle-col"]//table//tr'

        title = sel.xpath(titleSelector)
        links = sel.xpath(linkSelector)

        curyear = 0

        for i in range(1, len(links)):
            url = ''

            year = links[i].xpath('td//strong/text()').extract()

            if (year):
                curyear = year[0].encode('ascii', 'ignore')

            year = curyear

            # There are three different ways the rows of the table are structured.
            # 1. within <td>
                        # 2. within <td><div>
                        # 3. within <td><p>
                        #
            # Search with each filter and scrape the files and titles that are
            # found
            comp1 = links[i].xpath('td/text()').extract()
            if (comp1):
                # clean up the titles
                comp1 = re.sub(' +', ' ', comp1[0]).rstrip().encode(
                    'ascii', 'ignore')
                comp1 = re.sub('[\\\?\*\"\.><\|\r\n]', '', comp1)
                comp1 = re.sub('[:\/]', '-', comp1)
                comp1 = comp1.replace(' - ', '').replace(' -', '')

            comp2 = links[i].xpath('td//div/text()').extract()
            if (comp2):
                # clean up the titles
                comp2 = re.sub(' +', ' ', comp2[0]).rstrip().encode(
                    'ascii', 'ignore')
                comp2 = re.sub('[\\\?\*\"\.><\|\r\n]', '', comp2)
                comp2 = re.sub('[:\/]', '-', comp2)
                comp2 = comp2.replace(' - ', '').replace(' -', '')

            comp3 = links[i].xpath('td//p/text()').extract()
            if (comp3):
                # clean up the titles
                comp3 = re.sub(' +', ' ', comp3[0]).rstrip().encode(
                    'ascii', 'ignore')
                comp3 = re.sub('[\\\?\*\"\.><\|\r\n]', '', comp3)
                comp3 = re.sub('[:\/]', '-', comp3)
                comp3 = comp3.replace(' - ', '').replace(' -', '')

            comp = ''
            if (comp1):
                comp = comp1
            elif (comp2):
                comp = comp2
            elif (comp3):
                comp = comp3

            group = default(FILEGROUP)
            docs = links[i].xpath('td//div/a')
            for l in docs:
                if (l):
                    item = default(FILEITEM)
                    lastpart = l.xpath('text()').extract()[
                        0].rstrip().encode('ascii', 'ignore')
                    if (len(docs) == 1) or (len(docs) > 1 and 'PDF' not in lastpart):
                        url = l.xpath('@href').extract()[0]
                        url = urlparse.urljoin(response.url, url.strip())

                        name = comp + ' - ' + lastpart

                        logging.info(lastpart + ': ' + name)
                        item['source'] = url.encode('ascii', 'ignore').replace(' ', '%20')
                        item['name'] = name
                        item['state'] = state
                        item['year'] = year
                        group['items'].append(item)

            logging.info('SCRAPED > ' + str(len(group['items'])))
            yield group
