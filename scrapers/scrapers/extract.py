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

        i = lambda x: x

        def process_html_MA(f):
            crap = open(f['url']).read()
            crap = crap.replace('</html>','').replace('</body>','')
            # # logging.info(crap)
            soup = bs(crap)
            main = soup.select('div.bodyfield table table')
            f['raw_text'] = main[0].get_text(" ")
            # print soup.prettify()
            # get table in div with class bodyfield
            return f

        def process_html_ME(f):
            soup = bs(open(f['url']))
            main = soup.find('div', id='awt-content-area')
            f['raw_text'] = main.get_text()
            return f

        def process_pdf(spider, f):
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
            logging.info(
                'There are ' + str(len(os.listdir(direc))) + ' images extracted')
            for fi in os.listdir(direc):
                tes = subprocess.call(
                    ['tesseract', direc + fi, direc + 'output'])
                raw += open(direc + 'output.txt').read()

            shutil.rmtree(direc)

            f['raw_text'] = raw
            # logging.info(item)
            return f

        process_html = {
            'madoi': process_html_MA,
            'medoi': process_html_ME,
            'nhdoi': i,
            'ridoi': i,
            'vtdfr': i,
            'vtdoi': i,
            'ctdoimed': i
        }

        def process_file_item(f):
            try:
                if '.pdf' in f['source']:
                    f = process_pdf(spider, f)
                else:
                    f = process_html[spider.name](f)
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
