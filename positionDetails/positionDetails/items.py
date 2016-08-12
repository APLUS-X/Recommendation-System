# -*- coding: utf-8 -*-

from scrapy import Item,Field

class PositiondetailsItem(Item):
    positionName = Field()
    company = Field()
    city = Field()
    experience = Field()
    positionType = Field()
    salary = Field()
    description = Field()
    link = Field()
    publishedTime = Field()


