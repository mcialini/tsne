import logging
import scrapers.config as config
import os
import tempfile
import subprocess
import shutil


def process_HTML(item):
    print '\tHTML'
    return item

def process_PDF(spider, item):
    #     create a tmp directory inside the files_store
    direc = config.files_store + config.directory[spider.name] + 'tmp/'
    try:
        os.makedirs(direc)
    except Exception as e:
        logging.error(e.message)
        logging.error('Dropping file!')


    ret = subprocess.call([config.imgmagick, '-density', '400', item['url'], direc + 'file.jpg'])
    raw = ''
    for f in os.listdir(direc):
        print direc + f
        tes = subprocess.call(['tesseract', direc + f, direc + 'output'])
        raw += open(direc+'output.txt').read()

    shutil.rmtree(direc)

    item['raw_text'] = raw
    # logging.info(item)
    return item


class ExtractionPipeline(object):

    def process_item(self, item, spider):
        logging.info('EXTRACTING PIPELINE')
        try:
            if '.pdf' in item['source']:
                process_PDF(spider, item)
            else:
                item = process_HTML(item)
            return item
        except Exception as e:
            logging.error(e)
            logging.error('Dropping item!')
