import os
import logging
import requests
import shutil
import psycopg2
import urllib2

import scrapers.config as config


class DownloadingPipeline(object):

    def process_item(self, item, spider):
    	logging.info('DOWNLOADING PIPELINE')

        url, ext = os.path.splitext(item['source'])
        path = config.files_store + \
            config.directory[spider.name] + item['year'] + '/'

        try:
            os.makedirs(path)
        except Exception:  # Directories already exist
            pass

        try:
            # r = config.s.get(item['source'])
            req = urllib2.Request(item['source'])
            r = urllib2.urlopen(req)
            filename = (path + item['name'])[:251] + ext
            with open(filename, 'wb') as out_file:
                out_file.write(r.read())
            item['url'] = filename
        except Exception as e:
            logging.error(e)

        # logging.info(item)
        
        return item
