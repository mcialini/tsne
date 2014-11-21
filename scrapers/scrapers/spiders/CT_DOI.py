from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.spider import Spider, BaseSpider
from scrapy.http import Request, FormRequest

from scrapers.items import default, FILEGROUP, FILEITEM
import scrapers.config as config
import logging

import re
import urlparse


DOMAIN = 'catalog.state.ct.us'
URL = 'http://%s' % DOMAIN
state = 'CT'


urls = ['http://www.catalog.state.ct.us/cid/portalApps/EnforcementAction.aspx']


class CT_DOI_Spider(CrawlSpider):

    name = 'ctdoi'
    allowed_domains = [DOMAIN]

    start_urls = urls

    def parse(self, response):

        sel = Selector(response)

        """
        parse should grab all the data on a given page, then create a 
        formrequest for the next page with a callback of parse
        """
        rowSelector = '//table[@id="GridView1"]//tr'
        rows = sel.xpath(rowSelector)

        logging.info('********CALLED PARSE*********')
        for r in range(1, len(rows)-2):
            # The last row is the footer
            item = default(FILEITEM)
            group = default(FILEGROUP)
            cols = rows[r].xpath('td')
            name = cols[0].xpath('text()').extract()[0].encode('ascii', 'ignore').upper()
            disp = cols[1].xpath('text()').extract()[0].encode('ascii', 'ignore')
            date = cols[2].xpath('text()').extract()[0].encode('ascii', 'ignore')
            y = re.compile('\d\d\d\d')
            year = y.findall(date)[0].encode('ascii', 'ignore')
            type = cols[3].xpath('text()').extract()[0].encode('ascii', 'ignore')
            link = cols[4].xpath('a')
            url = link.xpath('@href').extract()[0]
            title = 'Disposition'

            item['source'] = url
            item['name'] = name
            item['state'] = state
            item['year'] = year

            group['items'].append(item)
            logging.info(item['name'])
            item = default(FILEITEM)


        viewStateSelector = '//input[@name="__VIEWSTATE"]/@value'
        viewState = sel.xpath(viewStateSelector).extract()[0].encode('ascii','ignore')
        eventValidationSel = '//input[@name="__EVENTVALIDATION"]/@value'
        eventValidation = sel.xpath(eventValidationSel).extract()[0]
        # print viewState
        resp =  FormRequest.from_response(
                response,
                formname="form1",
                formdata={
                    '__EVENTTARGET': 'GridView1',
                    '__EVENTARGUMENT': 'Page$Next',
                    '__EVENTVALIDATION': eventValidation,
                    '__VIEWSTATE': viewState.replace('%2','/'),
                    'ctl00$jsCheck' : str(0)
                },
                callback=self.dostuff,
                method='POST',
                dont_filter=True
            )

        logging.info(resp.headers)
        logging.info(resp.body)

    def dostuff(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response)
        sel = Selector(response)
        rowSelector = '//table[@id="GridView1"]//tr'
        rows = sel.xpath(rowSelector)

        logging.info('---------CALLED PARSE*********')
        for r in range(1, len(rows)-2):
            # The last row is the footer
            item = default(FILEITEM)
            group = default(FILEGROUP)
            cols = rows[r].xpath('td')
            name = cols[0].xpath('text()').extract()[0].encode('ascii', 'ignore').upper()
            disp = cols[1].xpath('text()').extract()[0].encode('ascii', 'ignore')
            date = cols[2].xpath('text()').extract()[0].encode('ascii', 'ignore')
            y = re.compile('\d\d\d\d')
            year = y.findall(date)[0].encode('ascii', 'ignore')
            type = cols[3].xpath('text()').extract()[0].encode('ascii', 'ignore')
            link = cols[4].xpath('a')
            url = link.xpath('@href').extract()[0]
            title = 'Disposition'

            item['source'] = url
            item['name'] = name
            item['state'] = state
            item['year'] = year

            group['items'].append(item)
            logging.info(item['name'])
            item = default(FILEITEM)