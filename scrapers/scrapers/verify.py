import hashlib, urllib2
from scrapers.config import *
import logging
from scrapy.exceptions import DropItem


class VerificationPipeline(object):
    def process_item(self, item, spider):
    # first just check if the source url exists kn the db
        logging.info('VERIFICATION PIPELINE!')
        data = (item['source'],)
        sql = "SELECT * FROM files WHERE source = %s"
        dbcur.execute(sql, data)
        if dbcur.fetchone() is not None:
            logging.info('URL test failed!')
            logging.info('Dropping file: ' + item['source'])
            raise DropItem()
        else:
            remote = urllib2.urlopen(item['source'])
            hash = hashlib.md5()

            total_read = 0
            while True:
                data = remote.read(4096)
                total_read += 4096

                if not data or total_read > 1024*1024:  # cutoff set to 1MB
                    break

                hash.update(data)

            checksum = hash.hexdigest()

            sql = "SELECT id FROM files WHERE checksum = (%s)"
            data = (checksum,)
            result = dbcur.execute(sql, data)
            if result is not None:
                logging.info('Checksum test failed!')
                logging.info('Dropping file: ' + item['source'])
            else:
                item['checksum'] = checksum
                return item