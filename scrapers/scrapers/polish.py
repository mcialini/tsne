import logging
import scrapers.config as config
import unicodedata
import re
from scrapers.regex import *

class PolishingPipeline(object):

    def process_item(self, item, spider):
        def process_file_item(f):
            """
            SPACE = ' +'
            VOWEL = ' (.*[aeiou]{4,}.*)'
            CONS  = ' (.*[bcdfghjklmnpqrstvwxyz]{5,}.*)'
            """
            try:
                raw = ''
                raw = f['raw_text'].replace('\n',' ').decode('string_escape').decode('utf-8')
                raw = unicodedata.normalize('NFKD', raw).encode('ascii', 'ignore')
                raw = re.sub(SPACE, ' ', raw)
                raw = re.sub(VOWEL + '|' + CONS, '', raw)
            except Exception as e:
                logging.error('Polish failed!' + str(e))

            f['raw_text'] = raw
            return f

        item['items'] = [i for i in map(process_file_item, item['items']) if i is not None]
        logging.info('POLISHING >' + str(len(item['items'])))
        if len(item['items']) > 0:
            return item