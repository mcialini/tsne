import logging
import scrapers.config as config
import unicodedata
import re
from scrapers.regex import *
from scrapy.exceptions import DropItem

class PolishingPipeline(object):

    def process_item(self, item, spider):
        def process_file_item(f):

            raw = ''
            try:
                raw = f['raw_text'].replace('\n',' ')
                if '.pdf' in f['source']:
                    raw = raw.decode('string_escape')
                    raw = raw.decode('utf-8')
                raw = unicodedata.normalize('NFKD', raw).encode('ascii', 'ignore')
                raw = re.sub(SPACE, ' ', raw)
                raw = re.sub(VOWEL + '|' + CONS, '', raw)
            except Exception as e:
                logging.error('Polish failed!' + str(e))
                logging.warning('Dropping file: ' + f['source'])

            f['raw_text'] = raw
            # if raw == '':
            #     logging.warning('RAW TEXT IS EMPTY FOR ' + f['url'])
            #     # print 'RAW TEXT IS EMPTY FOR ' + f['url']
            return f

        item['items'] = [i for i in map(process_file_item, item['items']) if i is not None]
        logging.info('POLISHED > ' + str(len(item['items'])))
        if len(item['items']) == 0:
            raise DropItem("Group has been dropped")
        else:
            logging.info(item['items'])
            return item