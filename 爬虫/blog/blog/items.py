from scrapy.item import Item, Field


class Website(Item):

    headTitle = Field()
    description = Field()
    url = Field()