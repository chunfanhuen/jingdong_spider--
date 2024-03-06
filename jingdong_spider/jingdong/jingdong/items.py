# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    comment = scrapy.Field()
    phone_link = scrapy.Field()
    stone_name = scrapy.Field()
    stone_link = scrapy.Field()
    pass
