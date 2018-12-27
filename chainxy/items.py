# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ChainItem(Item):

    name = Field()

    email = Field()

    phone = Field()

    website = Field()

    address1 = Field()

    address2 = Field()

    city = Field()

    state = Field()

    zipcode = Field()

    photo = Field()

    specialty = Field()

    latitude = Field()

    longitude = Field()





