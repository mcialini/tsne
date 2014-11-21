import os
import logging
import requests
import shutil
import psycopg2
import urllib2

import scrapers.config as config
from scrapy.exceptions import DropItem


class DownloadingPipeline(object):

    def process_item(self, item, spider):

        def process_file_item(f):
            url, ext = os.path.splitext(f['source'])
            path = config.files_store + \
                config.directory[spider.name] + f['year'] + '/'

            try:
                os.makedirs(path)
            except Exception:  # Directories already exist
                pass

            try:
                req = urllib2.Request(f['source'])
                r = urllib2.urlopen(req)
                filename = (path + f['name'])[:251] + ext
                with open(filename, 'wb') as out_file:
                    out_file.write(r.read())
                f['url'] = filename
            except Exception as e:
                logging.error('Download failed!')
                logging.error(e)
                logging.warning('Dropping file: ' + f['source'])
                return None
            
            return f

        item['items'] = [i for i in map(process_file_item, item['items']) if i is not None]
        logging.info('DOWNLOADED > ' + str(len(item['items'])))
        if len(item['items']) == 0:
            raise DropItem("Group has been dropped")
        else:
            return item
