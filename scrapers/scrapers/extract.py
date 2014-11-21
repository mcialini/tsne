import logging
import scrapers.config as config
import os
import tempfile
import subprocess
import shutil
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup as bs


class ExtractionPipeline(object):

    def process_item(self, item, spider):
        def process_HTML(f):
            print f['url']
            soup = bs(open(f['url']))
            print soup.head.title
            return f

        def process_PDF(spider, f):
            #     create a tmp directory inside the files_store
            direc = config.files_store + config.directory[spider.name] + 'tmp/'
            try:
                os.makedirs(direc)
            except Exception as e:
                logging.warning('Make dirs failed!')
                logging.error(e.message)
                logging.warning('Dropping file: ' + f['source'])

            ret = subprocess.call(
                [config.imgmagick, '-density', '400', f['url'], direc + 'file.jpg'])
            raw = ''
            logging.info('There are ' + str(len(os.listdir(direc))) + ' images extracted')
            for fi in os.listdir(direc):
                tes = subprocess.call(
                    ['tesseract', direc + fi, direc + 'output'])
                raw += open(direc + 'output.txt').read()

            shutil.rmtree(direc)

            f['raw_text'] = raw
            # logging.info(item)
            return f

        def process_file_item(f):
            try:
                if '.pdf' in f['source']:
                    f = process_PDF(spider, f)
                else:
                    f = process_HTML(f)
                return f
            except Exception as e:
                logging.error(e)
                logging.warning('Dropping file: ' + f['source'])
                return None

        item['items'] = [
            i for i in map(process_file_item, item['items']) if i is not None]
        logging.info('EXTRACTED > ' + str(len(item['items'])))
        if len(item['items']) == 0:
            raise DropItem("Group has been dropped")
        else:
            return item
