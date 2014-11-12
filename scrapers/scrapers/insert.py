import logging
from scrapers.config import *

class InsertionPipeline(object):
    def process_item(self, item, spider):
        logging.info('INSERTION PIPELINE')
        logging.info(item)
        try:
        	dbcur.execute("INSERT INTO files (url,source,name,state,year,gid,checksum,raw_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (item['url'], item['source'], item['name'], item['state'], int(item['year']), 0, item['checksum'], item['raw_text']))
        except Exception as e:
        	logging.error(e)
        conn.commit()
        return item