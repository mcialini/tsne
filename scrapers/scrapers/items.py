# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class GroupItem(Item):
	items = Field()

class FileItem(Item):
    url = Field()
    source = Field()
    name = Field()
    state = Field()
    year = Field()
    gid = Field()
    grouped = Field()
    checksum = Field()
    raw_text = Field()
