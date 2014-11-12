import logging
import scrapers.config as config
import unicodedata
import re

class PolishingPipeline(object):
    def process_item(self, item, spider):
        logging.info('POLISHING PIPELINE')

        SPACE = ' +'
        VOWEL = ' (.*[aeiou]{4,}.*)'
        CONS  = ' (.*[bcdfghjklmnpqrstvwxyz]{5,}.*)'

        try:
            raw = item['raw_text'].replace('\n',' ').decode('string_escape').decode('utf-8')
            raw = unicodedata.normalize('NFKD', raw).encode('ascii', 'ignore')
            raw = re.sub(SPACE, ' ', raw)
            raw = re.sub(VOWEL + '|' + CONS, '', raw)
        except Exception as e:
            print e
        item['raw_text'] = raw
        logging.info(item)
        return item