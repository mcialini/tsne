import logging
from scrapers.config import *


class InsertionPipeline(object):

    def process_item(self, item, spider):
        """
        Grab the next group id for this group of files, then insert each one
        individually
        """

        def process_file_item(f):
            try:
                sql_insert = "\
            		INSERT INTO files (\
            			url, \
            			source, \
            			name, \
            			state, \
            			year, \
            			gid, \
            			checksum, \
            			raw_text) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                dbcur.execute(
                    sql_insert,
                    (
                        f['url'],
                        f['source'],
                        f['name'],
                        f['state'],
                        int(f['year']),
                        gid,
                        f['checksum'],
                        f['raw_text']
                    )
                )
            except Exception as e:
                logging.warning('Insert failed!' + str(e))
                logging.warning('Dropping file: ' + f['source'])
                return None

            conn.commit()
            return f

        sql_get_group = "SELECT nextval('files_gid_seq')"
        dbcur.execute(sql_get_group)
        gid = dbcur.fetchone()

        item['items'] = [i for i in map(process_file_item, item['items']) if i is not None]
        logging.info('INSERTED > ' + str(len(item['items'])))
        logging.info(item['items'])
        return item


