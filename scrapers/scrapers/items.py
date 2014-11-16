# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

FILEITEM = 0
FILEGROUP = 1


class FileGroup(Item):
    items = Field()


class FileItem(Item):
    url = Field()
    source = Field()
    name = Field()
    state = Field()
    year = Field()
    gid = Field()
    checksum = Field()
    raw_text = Field()


def default(type):
    if type == 0:
        return FileItem(
            source='',
            name='',
            state='',
            year='',
            gid=None,
            checksum='',
            raw_text=''
        )
    elif type == 1:
        return FileGroup(items=[])
    else:
        return None
