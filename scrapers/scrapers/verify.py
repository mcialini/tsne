import hashlib, urllib2
from scrapers.config import *
from scrapy.exceptions import DropItem
import logging


class VerificationPipeline(object):
    def process_item(self, item, spider):
        def process_file_item(f):
            """
            Filters out all file items that have already been added to the database.
            1. Drop all file items whose source already exists
            2. Drop all file items whose checksum already exists
            """
            data = (f['source'],)
            sql = "SELECT * FROM files WHERE source = %s"
            dbcur.execute(sql, data)
            if dbcur.fetchone() is not None:
                logging.warning('URL test failed!')
                logging.warning('Dropping file: ' + f['source'])
                return None
            else:
                remote = urllib2.urlopen(f['source'])
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
                    logging.warning('Checksum test failed!')
                    logging.warning('Dropping file: ' + f['source'])
                    return None
                else:
                    f['checksum'] = checksum
                    return f

        item['items'] = [i for i in map(process_file_item, item['items']) if i is not None]
        logging.info('VERIFIED > ' + str(len(item['items'])))
        if len(item['items']) == 0:
            raise DropItem("Group has been dropped")
        else:
            return item

